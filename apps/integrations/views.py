import logging
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.exceptions import AuthenticationFailed, ParseError, APIException

from .actions import get_integration, get_org_id_and_name_from_access_token
from .models import Integration
from .serializers import IntegrationSerializer


logger = logging.getLogger(__name__)
logger.level = logging.INFO



class IntegrationsView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = []
    authentication_classes = []
    pagination_class = None
    serializer_class = IntegrationSerializer
    pagination_class = None
    queryset = Integration.objects.filter(is_active=True, is_beta=True).exclude(tpa_name='Sage File Export Integration').order_by('type', '-updated_at')
    filterset_fields = {'type': {'exact'}, 'org_id': {'exact'}}

    def get_object(self):
        queryset = self.get_queryset()
        instance = queryset.filter(
            org_id=self.request.data['org_id'],
            tpa_name=self.request.data['tpa_name']
        ).first()

        return instance

    def get(self, request, *args, **kwargs):
        # This block is for authenticating the user
        http_authorization = self.request.META.get('HTTP_AUTHORIZATION')
        if not http_authorization:
            raise AuthenticationFailed('No access token provided')

        access_token = http_authorization.split(' ')[1]
        try:
            org_id = get_org_id_and_name_from_access_token(access_token)['id']

            # Add validated org_id to query_params
            request.query_params._mutable = True
            request.query_params['org_id'] = org_id
            return super().get(request, *args, **kwargs)
        except Exception as error:
            logger.info(error)
            raise AuthenticationFailed('Invalid access token')


    def patch(self, request, *args, **kwargs):
        if request.data.get('tpa_name', None) is None:
            raise ParseError('tpa_name is required')

        http_authorization = self.request.META.get('HTTP_AUTHORIZATION')
        if not http_authorization:
            raise AuthenticationFailed('No access token provided')

        access_token = http_authorization.split(' ')[1]

        try:
            org_id = get_org_id_and_name_from_access_token(access_token)['id']
            request.data['org_id'] = org_id
        except Exception as error:
            logger.info(error)
            raise AuthenticationFailed('Invalid access token')

        # Silently ignore if the integration doesn't exist - sandbox cases
        if self.get_object() is None:
            return Response(
                data={
                    'message': 'Integration is inactive or does not exist'
                },
                status=status.HTTP_200_OK
            )

        try:
            return super().patch(request, *args, **kwargs)
        except Exception as error:
            logger.info(error)
            raise APIException('Something went wrong')


    def delete(self, request, *args, **kwargs):
        if request.data.get('tpa_name', None) is None:
            raise ParseError('tpa_name is required')

        http_authorization = self.request.META.get('HTTP_AUTHORIZATION')

        if not http_authorization:
            return Response(
                data={
                    'message': 'No access token provided'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = http_authorization.split(' ')[1]

        try:
            # The org id will be used in get_object to find the record to delete
            org_id = get_org_id_and_name_from_access_token(access_token)['id']
            request.data['org_id'] = org_id
        except Exception as error:
            logger.info(error)
            raise AuthenticationFailed('Invalid access token')

        if self.get_object() is None:
            raise ParseError('Integration is inactive or does not exist')

        try:
            return super().delete(request, *args, **kwargs)
        except Exception as error:
            logger.info(error)
            raise APIException('Something went wrong')

    def perform_create(self, serializer):
        try:
            access_token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            org = get_org_id_and_name_from_access_token(access_token)

            serializer.save(org_id=org['id'], org_name=org['name'])
        except Exception as error:
            logger.info(error)
            raise AuthenticationFailed('Invalid access token')
