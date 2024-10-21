from typing import List, Dict
import requests
import json

from connectors.travelperk.exceptions import *


class ApiBase:
    """The base class for all API classes."""

    GET_INVOICE_PROFILES = '/profiles'

    def __init__(self):
        self.__access_token = None
        self.__server_url = None

    def change_access_token(self, access_token):
        """Change the old access token with the new one.

        Parameters:
            access_token (str): The new access token.
        """
        self.__access_token = access_token

    def set_server_url(self, server_url):
        """Set the server URL dynamically upon creating a connection

        Parameters:
            server_url(str): The current server URL
        """
        self.__server_url = server_url

    def _get_error(self, status_code: int, response_text: str):
        """Get the error object from the response.

        Parameters:
            status_code (int): The status code of the response.
            response_text (str): The response text.

        Returns:
            The error object.
        """
        error_map = {
            400: BadRequestError('Something wrong with the request body', response_text),
            401: UnauthorizedClientError('Wrong client secret or/and refresh token', response_text),
            404: NotFoundError('Client ID doesn\'t exist', response_text),
            500: InternalServerError('Internal server error', response_text),
            409: BadRequestError('The webhook already exists', response_text)
        }

        return error_map.get(status_code, TravelperkError('Error: {0}'.format(status_code), response_text))

    def _get_request(self, object_type: str, api_url: str, params: dict = {}) -> List[Dict] or Dict:
        """Create a HTTP GET request.

        Parameters:
            api_url (str): Url for the wanted API.

        Returns:
            A response from the request (dict).
        """

        api_headers = {
            'Authorization': 'Bearer {0}'.format(self.__access_token),
            'Accept': 'application/json',
            'Api-Version': '1'
        }

        response = requests.get(
            '{0}{1}'.format(self.__server_url, api_url),
            headers=api_headers,
            params=params
        )

        if response.status_code == 200:
            result = json.loads(response.text)
            return result[object_type]
        else:
            raise self._get_error(response.status_code, response.text)

    def get_all_generator(self):
        """
        Creates a generator that contains all profiles across all pages
        
        Parameters:
            object_type (str): The type of object to get
            api_url (str): The url for the wanted API
            params (dict): The parameters for the request

        Returns:
            Generator with all objects of type `object_type`
        """

        limit = 50
        params = {'limit': limit}
        total_profiles = self._get_request('total', self.GET_INVOICE_PROFILES, params=params)

        for offset in range(0, total_profiles, limit):
            params['offset'] = offset
            profiles = self._get_request('profiles', self.GET_INVOICE_PROFILES, params=params)
            for profile in profiles:
                print('[x]', profile['name'])
                yield profile

    def _post_request(self, api_url: str, data: Dict) -> Dict:
        """Create a HTTP POST request.

        Parameters:
            api_url (str): Url for the wanted API.
            data (dict): The parameters for the request.

        Returns:
            A response from the request (dict).
        """

        api_headers = {
            'Authorization': 'Bearer {0}'.format(self.__access_token),
            'Accept': 'application/json',
            'Api-Version': '1'
        }

        response = requests.post(
            '{0}{1}'.format(self.__server_url, api_url),
            headers=api_headers,
            json=data
        )

        if response.status_code == 200:
            result = json.loads(response.text)
            return result

        else:
            raise self._get_error(response.status_code, response.text)

    def _delete_request(self, api_url: str) -> Dict:
        """Create a HTTP DELETE request.

        Parameters:
            api_url (str): Url for the wanted API.

        Returns:
            A response from the request (dict).
        """

        api_headers = {
            'Authorization': 'Bearer {0}'.format(self.__access_token),
            'Accept': 'application/json',
            'Api-Version': '1'
        }

        response = requests.delete(
            '{0}{1}'.format(self.__server_url, api_url),
            headers=api_headers
        )

        if response.status_code == 200:
            return response.text

        else:
            raise self._get_error(response.status_code, response.text)
