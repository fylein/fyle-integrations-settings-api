"""
Workato SDK Connector For Recipes
"""
from .api_base import ApiBase


class Recipes(ApiBase):
    """Class for Recipes xAPIs."""

    GET_MANAGED_USER = '/managed_users/{0}/recipes/'

    def get(self, managed_user_id):
        """
        Get all Recipes
        :return: List of Dicts in Recipes Schema
        """
        return self._get_request(Recipes.GET_MANAGED_USER.format(managed_user_id))
