import requests

from apps.users.helpers import get_cluster_domain

from .models import Integration


def get_integration(type: str, access_token: str):
    org_id = get_org_id_from_access_token(access_token)
    return Integration.objects.filter(org_id=org_id, type=type)


def get_org_id_from_access_token(access_token: str) -> str:
    headers: dict = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }

    cluster_domain = get_cluster_domain(access_token)

    response = requests.get('{}/platform/v1/spender/my_profile'.format(cluster_domain), headers=headers)

    if response.status_code == 200:
        my_profile = response.json()
        return my_profile['data']['org']['id']
    else:
        raise Exception(response.text)
