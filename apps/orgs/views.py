import logging


from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics

from apps.orgs.serializers import OrgSerializer
from apps.orgs.models import Org, User
from workato.workato import Workato


logger = logging.getLogger(__name__)
logger.level = logging.INFO

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
            parnter_org = Org.objects.get(user__in=[user], fyle_org_id=org_id)

            return Response(
                data=OrgSerializer(parnter_org).data,
                status=status.HTTP_200_OK
            )
        except Org.DoesNotExist:
            return Response(
                data={'message': 'Org Not Found'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self):
        return self.get(self)

class FyleConnection(generics.CreateAPIView):
    """
    Api Call to make Fyle Connection in workato
    """

    def post(self, request, *args, **kwargs):

        connector = Workato()
        managed_user_id = kwargs['managed_user_id']

        connections  = connector.connections.get(managed_user_id=managed_user_id)
        fyle_connection_id = connections['result'][1]['id']

        try:
            connection = connector.connections.put(
                managed_user_id=managed_user_id, 
                connection_id=fyle_connection_id,
                data=request.data
            )

        except Exception:
            return Response(
                data={
                    'message': 'Error in Creating Fyle Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )    

        return Response(
           connection,
           status=status.HTTP_200_OK
        )
