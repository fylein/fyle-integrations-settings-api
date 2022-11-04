from requests import Response

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import viewsets

from workato_connector.workato import Workato


class BambooHrConnection(viewsets.ViewSet):
    """
    API Call to make Bamboo HR Connection in workato
    """

    authentication_classes = []
    permission_classes = []

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

        except Exception:
            return Response(
                data={
                    'message': 'Error in Creating Bamboo HR Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class FyleConnection(viewsets.ViewSet):
    """
    Api Call to make Fyle Connection in workato
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):

        connector = Workato()
        managed_user_id=request.data['managed_user_id']
        connections = connector.connections.get(managed_user_id=managed_user_id)
        connection_id = connections['result'][0]['id']

        try:
            connection = connector.connections.put(
                managed_user_id=managed_user_id, 
                connection_id=connection_id,
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


class RecipeView(viewsets.ViewSet):
    """
    API Call to Get Fyle Recipe
    """

    authentication_classes = []
    permission_classes = []


    def get(self, request, *args, **kwargs):
        connector = Workato()
        managed_user_id=request.data['managed_user_id']
        recipes = connector.recipes.get(managed_user_id=managed_user_id)

        return Response(
           recipes,
           status=status.HTTP_200_OK
        )

    def get_by_id(self, request, *args, **kwargs):
        
        connector = Workato()
        managed_user_id=request.data['managed_user_id']
        recipe_id=kwargs['recipe_id']
        recipe_details = connector.recipes.get_by_id(managed_user_id, recipe_id)

        return Response(
            recipe_details,
            status=status.HTTP_200_OK
        )
