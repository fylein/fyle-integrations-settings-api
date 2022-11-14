from requests import Response

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import viewsets
from rest_framework import generics

from workato.workato import Workato


class BambooHrConnection(generics.CreateAPIView):
    """
    API Call to make Bamboo HR Connection in workato
    """

    def post(self, request, *args, **kwargs):
        connector = Workato()
        managed_user_id = request.data['managed_user_id']
        connection_id = request.data['connection_id']

        try:
            connection = connector.connections.put(
                managed_user_id=managed_user_id,
                connection_id=connection_id,
                data=request.data
            )

            return Response(
                data=connection,
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={
                    'message': 'Error in Creating Bamboo HR Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class RecipeView(generics.ListAPIView):
    """
    API Call to Get Fyle Recipe
    """

    def get_queryset(self, *args, **kwargs):
        connector = Workato()
        managed_user_id = kwargs['managed_user_id']
        recipes = connector.recipes.get(managed_user_id=managed_user_id)

        return Response(
           recipes,
           status=status.HTTP_200_OK
        )

