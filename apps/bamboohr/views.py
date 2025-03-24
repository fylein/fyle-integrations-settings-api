import logging
from apps.integrations.models import Integration
from bamboosdk.bamboohrsdk import BambooHrSDK

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics

from apps.orgs.models import Org
from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.bamboohr.serializers import BambooHrSerializer, BambooHrConfigurationSerializer
from apps.bamboohr.tasks import add_bamboo_hr_to_integrations, deactivate_bamboo_hr_integration, delete_sync_employee_schedule, invalidate_token_and_get_response

from bamboosdk.exceptions import InvalidTokenError, NoPrivilegeError, NotFoundItemError
from django_q.tasks import async_task

logger = logging.getLogger(__name__)
logger.level = logging.INFO

class HealthCheck(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        try:
            bamboohr = BambooHr.objects.get(org_id__in=[kwargs['org_id']])
        except BambooHr.DoesNotExist:
            return Response(
                data={'message': 'Bamboo HR Details Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            bamboohrsdk = BambooHrSDK(api_token=bamboohr.api_token, sub_domain=bamboohr.sub_domain)
            response = bamboohrsdk.time_off.get()
        except Exception:
            return invalidate_token_and_get_response(kwargs['org_id'])

        if response['timeOffTypes']:
            return Response(
                data = {
                    'message': 'Ready'
                },
                status=status.HTTP_200_OK
            )
        else:
            return invalidate_token_and_get_response(kwargs['org_id'])

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

        async_task('apps.bamboohr.tasks.update_employee', org_id, payload)

        return Response(
            {
                'status': 'success'
            },
            status=status.HTTP_201_CREATED
        )

class BambooHrConnection(generics.CreateAPIView):
    """
    API Call to make Bamboo HR Connection
    """

    def post(self, request, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()

        try:
            api_token = request.data['input']['api_token']
            sub_domain = request.data['input']['subdomain']
        except KeyError:
            return Response(
                data={
                    "message": "API_TOKEN and SUB_DOMAIN are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info('Bamboo HR Connection Request Payload | Content: {{api_token: {0}, sub_domain: {1}}}'.format(api_token, sub_domain))

        bamboohrsdk = BambooHrSDK(api_token=api_token, sub_domain=sub_domain)

        try:
            timeoff = bamboohrsdk.time_off.get()
        except (NoPrivilegeError, NotFoundItemError, InvalidTokenError) as e:
            return invalidate_token_and_get_response(kwargs['org_id'])

        logger.info('Bamboo HR Connection Timeoff Response | Content: {0}'.format(timeoff))
        if timeoff.get('timeOffTypes', None):
            bamboohr, _ = BambooHr.objects.update_or_create(org=org, defaults={
                'api_token': api_token,
                'sub_domain': sub_domain
            })

            add_bamboo_hr_to_integrations(org)

            return Response(
                data="BambooHr is connected",
                status=status.HTTP_200_OK
            )
        else:
            return invalidate_token_and_get_response(kwargs['org_id'])


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
    API call to disconnect bamboo connection
    """

    def post(self, request, *args, **kwargs):
        try:
            bamboohr_queryset = BambooHr.objects.filter(org__id=kwargs['org_id'])
            if bamboohr_queryset.count() == 0:
                return Response(
                    data = {
                        'message': 'BambooHR connection does not exists for this org.'
                    },
                    status = status.HTTP_404_NOT_FOUND
                )

            bamboohr_queryset.update(api_token=None, sub_domain=None)
            delete_sync_employee_schedule(org_id=kwargs['org_id'])
            deactivate_bamboo_hr_integration(kwargs['org_id'])
            return Response(
                data='Successfully Disconneted!',
                status=status.HTTP_200_OK
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
        async_task('apps.bamboohr.tasks.import_employees', kwargs['org_id'])

        return Response(
            data = {'message': 'success'},
            status=status.HTTP_201_CREATED
        )
