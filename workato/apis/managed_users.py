"""
Workato Connector For Managed User
"""
from .api_base import ApiBase

class ManagedUser(ApiBase):
    """Class for Managed Users xAPIs."""

    GET_MANAGED_USER = '/managed_users'
    POST_MANAGED_USER = '/managed_users'

    def get(self):
        """
        Get all Managed Users
        :return: List of Dicts in Managed User Schema
        """
        return self._get_request(ManagedUser.GET_MANAGED_USER)

    def post(self, data):
        """
        Post Managed User
        :return: Managed User Data
        """
        return self._post_request(ManagedUser.POST_MANAGED_USER, data)
