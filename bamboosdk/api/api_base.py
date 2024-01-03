import requests
import base64
import json
from bamboosdk.exceptions import *

class ApiBase:
    """
    Base class for all API classes
    """
    API_BASE_URL = 'https://api.bamboohr.com/api/gateway.php/{}'

    def __init__(self) -> None:
        self.__api_token = None
        self.__sub_domain = None
        self.headers = None
    
    def _get_request(self, module_api_path):
        """
        HTTP get method get data from BambooHR API URL

        Parameters:
            module_api_path (str): URL of BambooHR API
        """ 
        
        url = self.API_BASE_URL.format(self.__sub_domain) + module_api_path
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            result = json.loads(response.text)
            return result

        if response.status_code == 403:
            error_msg = json.loads(response.text)
            raise NoPrivilegeError('Forbidden, the user has insufficient privilege', error_msg)

        if response.status_code == 404:
            error_msg = json.loads(response.text)
            raise NotFoundItemError('Not found item with ID', error_msg)

        if response.status_code == 401:
            error_msg = 'The api token is invalid'
            raise InvalidTokenError('Invalid token, try to refresh it', error_msg)
        
        else:
            error_msg = json.loads(response.text)
            raise BambooHrSDKError('Status code {0}'.format(response.status_code), error_msg)

    
    def _post_request(self, module_api_path, payload):
        """
        HTTP post method to send data to BambooHR API URL

        Parameters:
            payload (dict): Data to be sent to Bamboo API
            module_api_path (str): URL of BambooHR API
        """  
    
        url= self.API_BASE_URL.format(self.__sub_domain) + module_api_path
        response = requests.post(url=url, json=payload, headers=self.headers)
        if response.status_code == 200:
            result = json.loads(response.text)
            return result

        if response.status_code == 201:
            result = json.loads(response.text)
            return result
        
        if response.status_code == 403:
            error_msg = json.loads(response.text)
            raise NoPrivilegeError('Forbidden, the user has insufficient privilege', error_msg)

        if response.status_code == 404:
            error_msg = json.loads(response.text)
            raise NotFoundItemError('Not found item with ID', error_msg)

        if response.status_code == 401:
            error_msg = 'The api token is invalid'
            raise InvalidTokenError('Invalid token, try to refresh it', error_msg)
        
        else:
            error_msg = json.loads(response.text)
            raise BambooHrSDKError('Status code {0}'.format(response.status_code), error_msg)
        
    def _delete_request(self, module_api_path):
        """
        HTTP delete method to delete resource on BambooHR

        Parameters:
            module_api_path (str): URL of BambooHR API
        """ 
        url= self.API_BASE_URL.format(self.__sub_domain) + module_api_path
        response = requests.delete(url=url, headers=self.headers)
        if response.status_code == 200:
            return {'message':'Web hook has been deleted'}

        if response.status_code == 403:
            error_msg = json.loads(response.text)
            raise NoPrivilegeError('Forbidden, the user has insufficient privilege', error_msg)

        if response.status_code == 404:
            error_msg = json.loads(response.text)
            raise NotFoundItemError('Not found item with ID', error_msg)

        if response.status_code == 401:
            error_msg = 'The api token is invalid'
            raise InvalidTokenError('Invalid token, try to refresh it', error_msg)
        
        else:
            error_msg = json.loads(response.text)
            raise BambooHrSDKError('Status code {0}'.format(response.status_code), error_msg)

    def __encode_username_password(self):
        """
        Utility method to be used in the header for authorization
        converts the api token and password to base64
        """

        payload = f'{self.__api_token}:a'
        payload = payload.encode()

        return base64.b64encode(payload).decode()

    def set_api_token(self, api_token):
        self.__api_token = api_token

        self.headers = {
            'Accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Basic {self.__encode_username_password()}'
        } 
    
    def set_sub_domain(self, sub_domain):
        self.__sub_domain = sub_domain
