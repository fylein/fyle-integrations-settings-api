from travelperksdk.exceptions import *

from typing import List, Dict
import requests
import json


class ApiBase:
    """The base class for all API classes."""

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

    def _get_request(self, object_type: str, api_url: str) -> List[Dict] or Dict:
        """Create a HTTP GET request.

        Parameters:
            api_url (str): Url for the wanted API.

        Returns:
            A response from the request (dict).
        """

        api_headers = {
            'Authorization': 'Bearer {0}'.format(self.__access_token),
            'Accept': 'application/json'
        }

        response = requests.get(
            '{0}{1}'.format(self.__server_url, api_url),
            headers=api_headers
        )

        if response.status_code == 200:
            result = json.loads(response.text)
            return result[object_type]

        elif response.status_code == 400:
            raise BadRequestError('Something wrong with the request body', response.text)

        elif response.status_code == 401:
            raise UnauthorizedClientError('Wrong client secret or/and refresh token', response.text)

        elif response.status_code == 404:
            raise NotFoundError('Client ID doesn\'t exist', response.text)

        elif response.status_code == 500:
            raise InternalServerError('Internal server error', response.text)

        else:
            raise TravelperkSDKError('Error: {0}'.format(response.status_code), response.text)
