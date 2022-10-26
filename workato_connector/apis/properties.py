"""
Workato Connector For Properties API
"""
from .api_base import ApiBase


class Properties(ApiBase):
    """Class for Properties xAPIs."""

    POST_PROPERTIES = '/api/managed_users/{0}/properties'
    GET_PROPERTIES = '/api/managed_users/{0}/properties'


    def get(self, managed_user_id):
        """
        Get All the Acccounting Properties for Managed User
        """
        return self._get_request(Properties.GET_PROPERTIES.format(managed_user_id))

    def post(self, managed_user_id, data):
        """
        Post Accounting Properties
        :return: List of Dicts in Connections Schema
        """
        return self._post_request(Properties.POST_PROPERTIES.format(managed_user_id), data=data)