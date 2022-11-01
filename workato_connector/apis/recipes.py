"""
Workato SDK Connector For Recipes
"""
from .api_base import ApiBase


class Recipes(ApiBase):
    """Class for Recipes xAPIs."""

    GET_RECIPES = '/managed_users/{0}/recipes/'
    GET_RECIPE_BY_ID = '/managed_users/{0}/recipes/{1}'
    POST_RECIPE = '/managed_users/{0}/recipes/{1}/{2}'

    def get(self, managed_user_id):
        """
        Get all Recipes
        :return: List of Dicts in Recipes Schema
        """
        return self._get_request(Recipes.GET_RECIPES.format(managed_user_id))

    def get_by_id(self, managed_user_id, recipe_id):
        """
        Get Recipe By ID
        :return: Get Recipe Details By ID
        """
        return self._get_request(Recipes.GET_RECIPE_BY_ID.format(managed_user_id, recipe_id))
    
    def post(self, managed_user_id, recipe_id, action):
        """
        Start And Stop API Connection
        """
        return self._put_request(Recipes.POST_RECIPE.format(managed_user_id, recipe_id, action))
