import logging
from typing import List, Dict
import requests
import json

from connectors.travelperk.exceptions import *

logger = logging.getLogger(__name__)

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

    def _get_error(self, status_code: int, response_text: str) -> TravelperkError:
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

        endpoint = '{0}{1}'.format(self.__server_url, api_url)
        logger.debug(f"GET {endpoint}")
        logger.debug(f"Params for GET request: {params}")
        response = requests.get(
            endpoint,
            headers=api_headers,
            params=params
        )

        if response.status_code == 200:
            result = json.loads(response.text)
            logger.debug(f"GET response: {result}")
            return result[object_type]
        else:
            error = self._get_error(response.status_code, response.text)
            logger.info(f"GET request failed: {response.status_code} | {error.message}")
            logger.info(f"GET response: {error.response}")
            raise error

    def _get_all_generator(self, object_type: str, api_url: str):
        """
        Creates a generator that contains all records of `object_type` across all pages
        
        Parameters:
            object_type (str): The type of object to get
            api_url (str): The url for the wanted API
            params (dict): The parameters for the request

        Returns:
            Generator with all objects of type `object_type`
        """

        limit = 50
        params = {'limit': limit}
        total_profiles = self._get_request('total', api_url, params=params)

        for offset in range(0, total_profiles, limit):
            params['offset'] = offset
            profiles = self._get_request(object_type, api_url, params=params)
            for profile in profiles:
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

        endpoint = '{0}{1}'.format(self.__server_url, api_url)
        logger.debug(f"POST {endpoint}")
        logger.debug(f"Payload for POST request: {data}")
        response = requests.post(
            endpoint,
            headers=api_headers,
            json=data
        )

        if response.status_code == 200:
            result = json.loads(response.text)
            logger.debug(f"POST response: {result}")
            return result

        else:
            error = self._get_error(response.status_code, response.text)
            logger.info(f"POST request failed: {response.status_code} | {error.message}")
            logger.info(f"POST response: {error.response}")
            raise error

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

        endpoint = '{0}{1}'.format(self.__server_url, api_url)
        logger.debug(f"DELETE {endpoint}")
        response = requests.delete(
            endpoint,
            headers=api_headers
        )

        if response.status_code == 200:
            logger.debug(f"DELETE response: {response.text}")
            return response.text
        else:
            error = self._get_error(response.status_code, response.text)
            logger.info(f"DELETE request failed: {response.status_code} | {error.message}")
            logger.info(f"DELETE response: {error.response}")
            raise error
