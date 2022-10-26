import os
import json
import string
import requests

API_URL = '{}/api/'.format(os.environ.get('VUE_APP_WK_ORIGIN'))

API_HEADERS: dict = {
    'X-USER-TOKEN': os.environ.get('WK_API_PLATFORM_KEY'),
    'X-USER-EMAIL': os.environ.get('WK_PARTNER_EMAIL'),
    'Content-Type': 'application/json'
}

class ApiBase:

    def _get_request(self, url: str, data: dict = None) -> requests.Response:
        """
        Get the response from the API.
        """

        response = requests.get('{}{}'.format(API_URL, url), json=data, headers=API_HEADERS)
        return json.loads(response.text)


    def _post_request(self, url: str, data: dict = None) -> requests.Response:
        """
        Post the data to the API.
        """

        response = requests.post('{}{}'.format(API_URL, url), headers=API_HEADERS, json=data)
        return json.loads(response.text)


    def _put_request(self, url: str, data: dict = None, action: string = None) -> requests.Response:
        """
        Post the data to the API.
        """

        if action:
            response = requests.put('{}{}/{}'.format(API_URL, url, action), headers=API_HEADERS)
        else:
            response = requests.put('{}{}'.format(API_URL, url), json=data, headers=API_HEADERS)

        return json.loads(response.text)

    def post_zip_file(self, url: str, file_path: str) -> requests.Response:
        """
        Post the data to the API.
        """
        headers = API_HEADERS.copy()
        headers['Content-Type'] = 'application/octet-stream'
        
        file = open(file_path, 'rb')

        response = requests.post('{}{}'.format(API_URL, url), headers=headers, data=file.read())
        return json.loads(response.text)
