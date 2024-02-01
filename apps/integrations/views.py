import logging
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.exceptions import AuthenticationFailed

from .actions import get_integration, get_org_id_and_name_from_access_token
from .models import Integration
from .serializers import IntegrationSerializer


logger = logging.getLogger(__name__)
logger.level = logging.INFO



class IntegrationsView(generics.ListCreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = IntegrationSerializer
    queryset = Integration.objects.filter(is_active=True, is_beta=True)
    filterset_fields = {'type': {'exact'}, 'org_id': {'exact'}}

    def get(self, request, *args, **kwargs):
        # This block is for authenticating the user
        access_token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            org_id = get_org_id_and_name_from_access_token(access_token)['id']

            # Add validated org_id to query_params
            request.query_params._mutable = True
            request.query_params['org_id'] = org_id
            return super().get(request, *args, **kwargs)
        except Exception as error:
            logger.info(error)
            raise AuthenticationFailed('Invalid access token')

    def perform_create(self, serializer):
        try:
            access_token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            org = get_org_id_and_name_from_access_token(access_token)

            serializer.save(org_id=org['id'], org_name=org['name'])
        except Exception as error:
            logger.info(error)
            raise AuthenticationFailed('Invalid access token')
