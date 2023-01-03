"""
Workato Connector For Managed User
"""
from .api_base import ApiBase

class ManagedUser(ApiBase):
    """Class for Managed Users xAPIs."""

    GET_MANAGED_USER = '/managed_users'
    GET_MANAGED_USER_BY_ID = '/managed_users/E{0}'
    POST_MANAGED_USER = '/managed_users'

    def get(self):
        """
        Get all Managed Users
        :return: List of Dicts in Managed User Schema
        """
        return self._get_request(ManagedUser.GET_MANAGED_USER)


    def get_by_id(self, org_id):
        """
        Get Managed User By Id
        :return: Dict in Managed User Schema
        """
        return self._get_request(ManagedUser.GET_MANAGED_USER_BY_ID.format(org_id))


    def post(self, data):
        """
        Post Managed User
        :return: Managed User Data
        """
        return self._post_request(ManagedUser.POST_MANAGED_USER, data)
