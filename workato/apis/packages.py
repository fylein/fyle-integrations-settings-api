"""
Workato Connector For Packages API
"""
from .api_base import ApiBase


class Packages(ApiBase):
    """Class for Packages xAPIs."""

    POST_PACKAGE = '/managed_users/{0}/imports?folder_id={1}?restart_recipes=true'
    GET_PACKAGE = '/managed_users/{0}/imports/{1}'


    def post(self, managed_user_id, folder_id, file_path):
        """
        Post Package To Workato
        """
        return self.post_zip_file(Packages.POST_PACKAGE.format(managed_user_id, folder_id), file_path)


    def get(self, managed_user_id, package_id):
        """
        Get Package From Workato
        """
        return self._get_request(Packages.GET_PACKAGE.format(managed_user_id, package_id))
