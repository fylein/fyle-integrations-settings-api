
import json, os
import pytest
from rest_framework.response import Response

from django.urls import reverse

from tests.helper import dict_compare_keys
from .fixtures import fixture

from django.conf import settings

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
    assert response.status_code == 404

    response = json.loads(response.content)
    assert response['message'] != None
    
@pytest.mark.django_db(databases=['default'])
def test_orgs_put_view(api_client, mocker, access_token):
    """
    Test Put of Partner Orgs
    """
    url = reverse('orgs')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.put(url)
    assert response.status_code == 200

@pytest.mark.django_db(databases=['default'])
def test_new_org_put_view(api_client, mocker, access_token):
    """
    Test Put of New Partner Org
    """
    mocker.patch(
        'apps.orgs.serializers.get_fyle_admin',
        return_value=fixture['my_profile_admin']
    )

    url = reverse('orgs')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.put(url)
    assert response.status_code == 200

@pytest.mark.django_db(databases=['default'])
def test_admin_view(api_client, mocker, access_token, get_org_id):
    """
    Test Admin View
    """
    url = reverse('admin-view',
        kwargs={
            'org_id':get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    mocker.patch(
        'fyle.platform.apis.v1beta.admin.employees.list_all',
        return_value=[fixture['users']]
    )

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data == [{ "email": "abc@ac.com", "name": "abc"}]
