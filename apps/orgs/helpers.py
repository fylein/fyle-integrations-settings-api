import json
from typing import Dict

import requests

from django.conf import settings


def post_request(url: str, body: Dict, access_token: str) -> Dict:
    """
    Create a HTTP post request.
    """
    api_headers = {}
    api_headers['content-type'] = 'application/json'
    api_headers['Authorization'] = 'Bearer {0}'.format(access_token)

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
    cluster_api_url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)

    return post_request(cluster_api_url, {}, access_token)['cluster_domain']
