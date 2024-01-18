import hashlib
import hmac
import json
import logging
from bamboosdk.bamboohrsdk import BambooHrSDK

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics

from workato.exceptions import *
from apps.orgs.models import Org
from apps.orgs.actions import create_connection_in_workato, post_folder, post_package
from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.bamboohr.serializers import BambooHrSerializer, BambooHrConfigurationSerializer
from apps.bamboohr.actions import disconnect_bamboohr, sync_employees
from apps.names import BAMBOO_HR

from django_q.tasks import async_task

logger = logging.getLogger(__name__)
logger.level = logging.INFO

class HealthCheck(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        try:
            bamboohr = BambooHr.objects.get(org_id__in=[kwargs['org_id']], is_credentials_expire=False)
            bamboohrsdk = BambooHrSDK(api_token=bamboohr.api_token, sub_domain=bamboohr.sub_domain)
            response = bamboohrsdk.time_off.get()

            if response['timeOffTypes']:
                return Response(
                    data = {
                        'message': 'Ready'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                bamboohr.is_credentials_expired = True
                bamboohr.save()
                return Response(
                    data = {
                        'message': 'Invalid token'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BambooHr.DoesNotExist:
            return Response(
                data={'message': 'Bamboo HR Details Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )

class BambooHrView(generics.ListAPIView):
    serializer_class = BambooHrSerializer

    def get(self, request, *args, **kwargs):
        try:
            bamboohr = BambooHr.objects.get(org_id__in=[kwargs['org_id']])
            return Response(
                data=BambooHrSerializer(bamboohr).data,
                status=status.HTTP_200_OK
            )
        except BambooHr.DoesNotExist:
            return Response(
                data={'message': 'Bamboo HR Details Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )

class WebhookCallbackAPIView(generics.CreateAPIView):

    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):

        org_id = kwargs['org_id']
        payload = request.data
        
        bamboohr = BambooHr.objects.get(org_id__in=[org_id])
        private_key = bamboohr.private_key
        timestamp = request.headers['X-BambooHR-Timestamp']
        signature = request.headers['X-BambooHR-Signature']

        if timestamp and signature:
            generated_signature = hmac.new(private_key.encode(), (json.dumps(payload)+ timestamp).encode(), hashlib.sha256).hexdigest()
            if hmac.compare_digest(generated_signature, signature):
                async_task('apps.bamboohr.tasks.update_employee', org_id, payload)
                return Response(
                    {
                        'status': 'success'
                    },
                status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        'status': 'Failed'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
                    {
                        'status': 'Failed'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

class BambooHrConnection(generics.CreateAPIView):
    """
    API Call to make Bamboo HR Connection in Workato
    """

    def post(self, request, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()

        api_token = request.data['input']['api_token']
        sub_domain = request.data['input']['subdomain']

        bamboohrsdk = BambooHrSDK(api_token=api_token, sub_domain=sub_domain)
        timeoff = bamboohrsdk.time_off.get()
        if timeoff.get('timeOffTypes', None):
            bamboohr, _ = BambooHr.objects.update_or_create(org=org, defaults={
                'api_token': api_token,
                'sub_domain': sub_domain
            })

            return Response(
            data="BambooHr is connected",
            status=status.HTTP_200_OK
        )
        else:
            return Response(
                data = {
                    'message': 'Invalid token'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class BambooHrConfigurationView(generics.ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        try:
            org_id = self.request.query_params.get('org_id')
            configuration = BambooHrConfiguration.objects.get(org__id=org_id)

            return Response(
                data=BambooHrConfigurationSerializer(configuration).data,
                status=status.HTTP_200_OK
            )

        except BambooHrConfiguration.DoesNotExist:
            return Response(
                data={'message': 'BambooHr Configuration does not exist for this Workspace'},
                status=status.HTTP_404_NOT_FOUND
            )
        
    def post(self, request, *args, **kwargs):
        try:
            org_id = self.request.data['org']

            configuration, _ = BambooHrConfiguration.objects.update_or_create(
            org_id=org_id,
            defaults={
                'additional_email_options': request.data['additional_email_options'],
                'emails_selected': request.data['emails_selected']
                }
            )

            return Response(
                data=BambooHrConfigurationSerializer(configuration).data,
                status=status.HTTP_200_OK
            )

        except BambooHrConfiguration.DoesNotExist:
            return Response(
                data={'message': 'BambooHr Configuration does not exist for this Workspace'},
                status=status.HTTP_404_NOT_FOUND
            )
        

    def get_object(self, *args, **kwargs):
        return self.get(self, *args, **kwargs)

class DisconnectView(generics.CreateAPIView):

    """
    API Call to Start And Stop a Recipe in Workato
    """

    def post(self, request, *args, **kwargs):
        try:
            bamboohr_queryset = BambooHr.objects.filter(org__id=kwargs['org_id'])
            bamboohr = bamboohr_queryset.first()
            bambamboohrsdk = BambooHrSDK(api_token=bamboohr.api_token, sub_domain=bamboohr.sub_domain)
            bambamboohrsdk.webhook.delete(id=bamboohr.webhook_id)
            bamboohr_queryset.update(api_token=None, sub_domain=None)
            return Response(
                data='Successfully Disconneted!',
                status=status.HTTP_200_OK
            )
        except BambooHr.DoesNotExist:
            return Response(
                data = {
                    'message': 'BambooHR connection does not exists for this org.'
                },
                status = status.HTTP_404_NOT_FOUND
            )
        except BambooHrConfiguration.DoesNotExist:
            return Response(
                data={'message': 'BambooHr Configuration does not exist for this Workspace'},
                status=status.HTTP_404_NOT_FOUND
            )


class SyncEmployeesView(generics.UpdateAPIView):
    
    """
    API To Sync Employees From BambooHr To Fyle
    """

    def post(self, request, *args, **kwargs):
    
        async_task('apps.bamboohr.tasks.refresh_employees', kwargs['org_id'])

        return Response(
            data = {'message': 'success'},
            status=status.HTTP_201_CREATED
        )
