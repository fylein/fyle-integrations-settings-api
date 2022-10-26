"""
Workato Connector For Packages API
"""
from .api_base import ApiBase


class Packages(ApiBase):
    """Class for Packages xAPIs."""

    POST_PACKAGE = '/managed_users/{0}/imports?folder_id={1}'


    def post(self, managed_user_id, folder_id):
        """
        Post Package To Workato
        """
        return self._post_request(Packages.POST_PACKAGE.format(managed_user_id, folder_id))
