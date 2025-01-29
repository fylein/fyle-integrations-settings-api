
import logging

from django_q.tasks import async_task
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics
from django_q.tasks import async_task

from django.contrib.auth import get_user_model

from apps.orgs.serializers import OrgSerializer
from apps.orgs.models import Org, User
from apps.orgs.actions import get_admin_employees

from admin_settings.utils import LookupFieldMixin
from apps.orgs.serializers import ExpenseAttributeSerializer
from apps.orgs.utils import import_categories
from apps.orgs.actions import get_admin_employees
from apps.fyle_hrms_mappings.models import ExpenseAttribute
from apps.names import *

logger = logging.getLogger(__name__)
logger.level = logging.INFO


User = get_user_model()


class ReadyView(generics.RetrieveAPIView):
    """
    Ready call
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Ready call
        """

        return Response(
            data={
                'message': 'Ready'
            },
            status=status.HTTP_200_OK
        )


class OrgsView(generics.RetrieveUpdateAPIView):
    """
    New Fyle Org
    """
    serializer_class = OrgSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(user_id=self.request.user)
            org_id = self.request.query_params.get('org_id')
            org = Org.objects.get(user__in=[user], fyle_org_id=org_id)

            return Response(
                data=OrgSerializer(org).data,
                status=status.HTTP_200_OK
            )
        except Org.DoesNotExist:
            return Response(
                data={'message': 'Org Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get_object(self):
        return self.get(self)


class WorkspaceAdminsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        """
        Get All Admins of this orgs
        """

        admin_employees = get_admin_employees(org_id=kwargs['org_id'], user=request.user)

        return Response(
            data=admin_employees,
            status=status.HTTP_200_OK
        )


class SyncCategories(generics.CreateAPIView):
    """
    API Call to Sync Categories in Workato
    """˳in

    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):

        async_task(import_categories, org_id=kwargs['org_id'])
        return Response(
            status=status.HTTP_200_OK
        )


class ExpenseAttributeView(LookupFieldMixin, generics.ListAPIView):
    """
    Destination Attributes view
    """

    queryset = ExpenseAttribute.objects.all()
    serializer_class = ExpenseAttributeSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {'attribute_type': {'exact', 'in'}, 'active': {'exact'}}
    ordering_fields = ('value',)
