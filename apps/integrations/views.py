import logging
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.exceptions import AuthenticationFailed

from .actions import get_integration, get_org_id_from_access_token
from .models import Integration
from .serializers import IntegrationSerializer


logger = logging.getLogger(__name__)
logger.level = logging.INFO



class IntegrationsView(generics.ListCreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = IntegrationSerializer
    queryset = Integration.objects.filter(is_active=True, is_beta=True)
    filterset_fields = {'type': {'exact'}}

    def perform_create(self, serializer):
        try:
            access_token = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            org_id = get_org_id_from_access_token(access_token)

            serializer.save(org_id=org_id)
        except Exception as error:
            logger.info(error)
            raise AuthenticationFailed('Invalid access token')
