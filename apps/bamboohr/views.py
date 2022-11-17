from requests import Response

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import viewsets
<<<<<<< HEAD

from workato_connector.workato import Workato


class BambooHrConnection(viewsets.ViewSet):
=======
from rest_framework import generics

from workato.workato import Workato


class BambooHrConnection(generics.CreateAPIView):
>>>>>>> 0082f3715dc041c8c98a6af68c737e20ac632dc1
    """
    API Call to make Bamboo HR Connection in workato
    """

<<<<<<< HEAD
    authentication_classes = []
    permission_classes = []

=======
>>>>>>> 0082f3715dc041c8c98a6af68c737e20ac632dc1
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

<<<<<<< HEAD
=======
            return Response(
                data=connection,
                status=status.HTTP_200_OK
            )

>>>>>>> 0082f3715dc041c8c98a6af68c737e20ac632dc1
        except Exception:
            return Response(
                data={
                    'message': 'Error in Creating Bamboo HR Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

<<<<<<< HEAD
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
=======
class RecipeView(generics.ListAPIView):
>>>>>>> 0082f3715dc041c8c98a6af68c737e20ac632dc1
    """
    API Call to Get Fyle Recipe
    """

<<<<<<< HEAD
    authentication_classes = []
    permission_classes = []


    def get(self, request, *args, **kwargs):
        connector = Workato()
        managed_user_id=request.data['managed_user_id']
=======
    def get_queryset(self, *args, **kwargs):
        connector = Workato()
        managed_user_id = kwargs['managed_user_id']
>>>>>>> 0082f3715dc041c8c98a6af68c737e20ac632dc1
        recipes = connector.recipes.get(managed_user_id=managed_user_id)

        return Response(
           recipes,
           status=status.HTTP_200_OK
        )

<<<<<<< HEAD
    def get_by_id(self, request, *args, **kwargs):
        
        connector = Workato()
        managed_user_id=request.data['managed_user_id']
        recipe_id=kwargs['recipe_id']
        recipe_details = connector.recipes.get_by_id(managed_user_id, recipe_id)

        return Response(
            recipe_details,
            status=status.HTTP_200_OK
        )
=======
>>>>>>> 0082f3715dc041c8c98a6af68c737e20ac632dc1
