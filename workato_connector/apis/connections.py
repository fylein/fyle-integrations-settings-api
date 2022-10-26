"""
Workato Connector For Connections
"""
from .api_base import ApiBase


class Connections(ApiBase):
    """Class for Connection xAPIs."""

    GET_CONNECTIONS = '/managed_users/{0}/connections'
    POST_CONNECTION = 'managed_users/{0}/connections/{1}'

    def get(self, managed_user_id):
        """
        Get all Connections
        :return: List of Dicts in Connections Schema
        """
        return self._get_request(Connections.GET_CONNECTIONS.format(managed_user_id))
    

    def put(self, managed_user_id, connection_id):
        """
        Create A Connection
        """
        return self._put_request(Connections.POST_CONNECTION.format(managed_user_id, connection_id))