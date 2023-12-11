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
    
    def __post_request(self, module_api_path):
        """
        HTTP post method to send data to BambooHR API URL

        Parameters:
            payload (dict): Data to be sent to Bamboo API
            module_api_path (str): URL of BambooHR API
        """

        headers = {
            "content-type": "application/json",
            "authorization": f"Basic {self.__encode_username_password()}"
        }   

        payload = { "fields": ["displayName", "firstName", "lastName", "department", "workEmail", "supervisorEmail", "status"] }
        
        url= self.API_BASE_URL.format(self.__sub_domain) + module_api_path
        response = requests.post(url=url, json=payload, headers=headers)
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
    
    def set_sub_domain(self, sub_domain):
        self.__sub_domain = sub_domain
