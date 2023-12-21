from django.conf import settings
import json
from typing import Dict
import requests
from fyle.platform import Platform


class PlatformConnector:
    """
    Fyle Platform utility functions
    """

    def __init__(self, refresh_token: str, cluster_domain: str):
        server_url = '{}/platform/v1'.format(cluster_domain)

        self.connection = Platform(
            server_url=server_url,
            token_url=settings.FYLE_TOKEN_URI,
            client_id=settings.FYLE_CLIENT_ID,
            client_secret=settings.FYLE_CLIENT_SECRET,
            refresh_token=refresh_token
        )

    def sync(self):
        query_params = {'is_enabled': 'eq.true','order': 'updated_at.desc'}
        attribute_type = 'EMPLOYEE'
        generator = self.connection.v1beta.admin.employees.list_all(query_params)
        for items in generator:
            employee_attributes = []
            for employee in items['data']:
                employee_attributes.append({
                        'attribute_type': attribute_type,
                        'display_name': attribute_type.replace('_', ' ').title(),
                        'value': employee['user']['email'],
                        'source_id': employee['id'],
                        'active': True,
                        'detail': {
                            'user_id': employee['user_id'],
                            'employee_code': employee['code'],
                            'full_name': employee['user']['full_name'],
                            'location': employee['location'],
                            'department': employee['department']['name'] if employee['department'] else None,
                            'department_id': employee['department_id'],
                            'department_code': employee['department']['code'] if employee['department'] else None
                        }
                    })
        
        # add employees to expense_attribute table

def post_request(url: str, body: Dict, api_headers: Dict) -> Dict:
    """
    Create a HTTP post request.
    """

    response = requests.post(
        url,
        headers=api_headers,
        data=body
    )

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(response.text)



def get_cluster_domain(access_token: str) -> str:
    """
    Get cluster domain name from fyle
    :param access_token: (str)
    :return: cluster_domain (str)
    """
    api_headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {0}'.format(access_token)
    }
    cluster_api_url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)

    return post_request(cluster_api_url, {}, api_headers)['cluster_domain']
