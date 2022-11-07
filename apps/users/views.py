import os
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from fyle_rest_auth.models import AuthToken

from apps.orgs.models import Org
from .helpers import PlatformConnector

class UserProfileView(generics.RetrieveAPIView):


    def get(self, request, *args, **kwargs):
        """
        Get User Profile
        """
        refresh_token = AuthToken.objects.get(user__user_id=request.user).refresh_token
        cluster_domain = Org.objects.get(user__user_id=request.user) .cluster_domain

        platform = PlatformConnector(refresh_token, cluster_domain)

        user_profile = platform.connection.v1beta.spender.my_profile.get()

        return Response(
            data=user_profile,
            status=status.HTTP_200_OK
        )
