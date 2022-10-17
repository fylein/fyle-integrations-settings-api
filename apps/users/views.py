from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class UserProfileView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get User Details
        """

        return Response(
            data={'Name': 'Fyle Admin Settings'},
            status=status.HTTP_200_OK
        )


