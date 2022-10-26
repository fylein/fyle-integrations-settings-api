"""
Workato SDK Connector For Folders
"""
from unicodedata import name
from .api_base import ApiBase


class Folders(ApiBase):
    """Class for Folders xAPIs."""

    POST_FOLDER = '/managed_users/{0}/folders'

    def post(self, managed_user_id, folder_name):
        """
        Get all Recipes
        :return: List of Dicts in Recipes Schema
        """
        data = {
            "name": folder_name
        }

        return self._post_request(Folders.POST_FOLDER.format(managed_user_id), data)