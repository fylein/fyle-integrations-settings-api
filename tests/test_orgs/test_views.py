import json, os
import pytest
from rest_framework.response import Response
from rest_framework import status

from django.urls import reverse

from tests.helper import dict_compare_keys
from .fixtures import fixture, expected_org_response

from django.conf import settings

@pytest.mark.django_db
def test_ready_view(api_client):
    """Test the ready endpoint returns 200 and correct message."""
    url = reverse('ready')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('message') == 'Ready'

@pytest.mark.django_db
def test_orgs_get_view_success(api_client, access_token):
    """Test GET orgs with valid org_id returns correct org data."""
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.get(url, {'org_id': 'orHVw3ikkCxJ'})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    expected = expected_org_response
    assert dict_compare_keys(expected, data) == [], 'orgs GET diff in keys'
    assert data['fyle_org_id'] == expected['fyle_org_id']
    assert data['name'] == expected['name']

@pytest.mark.django_db
def test_orgs_get_view_not_found(api_client, access_token):
    """Test GET orgs with invalid org_id returns 404."""
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.get(url, {'org_id': 'wrong_org_id'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'message' in response.json()

@pytest.mark.django_db
def test_orgs_get_view_missing_org_id(api_client, access_token):
    """Test GET orgs with missing org_id returns 404 or 400."""
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.get(url)
    # Depending on implementation, could be 404 or 400
    assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_orgs_get_view_unauthorized(api_client):
    """Test GET orgs without token returns 400."""
    url = reverse('orgs')
    response = api_client.get(url, {'org_id': 'orHVw3ikkCxJ'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_orgs_put_view(api_client, access_token, mocker):
    """Test PUT orgs returns 200 for valid request."""
    mocker.patch(
        'apps.orgs.serializers.get_fyle_admin',
        return_value={
            "data": {
                "org": {"currency": "EUR", "domain": "aafyle.in", "id": "orHVw3ikkCxK", "name": "Ashwin Org"},
                "org_id": "orHVw3ikkCxK",
                "roles": ["FYLER", "ADMIN"],
                "user": {"email": "ashwin.t+1@fyle.in", "full_name": "Joannaa", "id": "usqywo0f3nBZ"},
                "user_id": "usqywo0f3nBZ"
            }
        }
    )
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.put(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_new_org_put_view(api_client, mocker, access_token):
    """Test PUT orgs for new org with admin profile patch."""
    mocker.patch(
        'apps.orgs.serializers.get_fyle_admin',
        return_value={
            "data": {
                "org": {"currency": "EUR", "domain": "aafyle.in", "id": "orHVw3ikkCxK", "name": "Ashwin Org"},
                "org_id": "orHVw3ikkCxK",
                "roles": ["FYLER", "ADMIN"],
                "user": {"email": "ashwin.t+1@fyle.in", "full_name": "Joannaa", "id": "usqywo0f3nBZ"},
                "user_id": "usqywo0f3nBZ"
            }
        }
    )
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.put(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_admin_view(api_client, mocker, access_token, get_org_id):
    """Test GET admin view returns correct admin data."""
    url = reverse('admin-view', kwargs={'org_id': get_org_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    mocker.patch(
        'fyle.platform.apis.v1.admin.employees.list_all',
        return_value=[{
            "count": 1,
            "data": [{
                "user": {"email": "abc@ac.com", "full_name": "abc", "id": "usG6YgUWBHIG"},
                "user_id": "usG6YgUWBHIG"
            }],
            "offset": 0
        }]
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"email": "abc@ac.com", "name": "abc"}]
