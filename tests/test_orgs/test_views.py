
import json
import pytest
from django.urls import reverse

from tests.helper import dict_compare_keys
from .fixtures import fixture


@pytest.mark.django_db(databases=['default'])
def test_ready_view(api_client, mocker, access_token):
    """"
    Test Get of Ready state
    """
    url = reverse('ready')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db(databases=['default'])
def test_orgs_get_view(api_client, mocker, access_token):
    """
    Test Get of Orgs
    """
    url = reverse('orgs')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url, {'org_id': 'orHVw3ikkCxJ'})
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['orgs']) == [], 'orgs GET diff in keys'

    response = api_client.get(url, {'org_id': 'wrong_org_id'})
    assert response.status_code == 400

    response = json.loads(response.content)
    assert response['message'] != None
