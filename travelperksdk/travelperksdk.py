"""
Travelperk Python SDK
"""
import json
from typing import List, Dict
import requests
from future.moves.urllib.parse import urlencode


class TravelperkSDK:
    """
    Travelperk SDK
    """

    def __init__(self, client_id: str, client_secret: str,
                 refresh_token: str, environment: str):
        """
        Initialize connection to Travelperk
        :param client_id: Travelperk client_Id
        :param client_secret: Travelperk client_secret
        :param refresh_token: Travelperk refresh_token
        :param environment: production or sandbox
        """
        # Initializing variables
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.refresh_token = refresh_token

        if environment.lower() == 'sandbox':
            self.__base_url = 'https://api.sandbox-travelperk.com'
            self.__token_url = 'https://app.sandbox-travelperk.com/accounts/oauth2/token/'
        elif environment.lower() == 'production':
            self.__base_url = 'https://api.travelperk.com'
            self.__token_url = 'https://app.travelperk.com/accounts/oauth2/token/'
        else:
            raise ValueError('environment can only be prodcution / sandbox')

        self.__access_token = None

        self.update_access_token()
        self.update_server_url()

    def update_server_url(self):
        """
        Update the server url in all API objects.
        """
        base_url = self.__base_url

        self.invoices.set_server_url(base_url)

    def update_access_token(self):
        """
        Update the access token and change it in all API objects.
        """
        self.__get_access_token()
        access_token = self.__access_token

        self.invoices.change_access_token(access_token)

    def __get_access_token(self):
        """Get the access token using a HTTP post.

        Returns:
            A new access token.
        """

        api_data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }

        api_data = urlencode(api_data)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url=self.__token_url, data=api_data, headers=headers)

        if response.status_code == 200:
            auth = json.loads(response.text)
            self.__access_token = auth['access_token']
            self.refresh_token = auth['refresh_token']

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
