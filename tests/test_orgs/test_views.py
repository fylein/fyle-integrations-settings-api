import json
import pytest
from django.urls import reverse
from rest_framework import status

from tests.helper import dict_compare_keys
from .fixtures import fixture
from .mock_setup import mock_get_fyle_admin, mock_platform_employees_list


def test_ready_view_case_1(mock_dependencies, api_client, db):
    """
    Test ready view
    Case: Returns 200 for health check
    """
    url = reverse('ready')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_orgs_get_view_case_1(mock_dependencies, api_client, access_token):
    """
    Test orgs GET view
    Case: Valid org_id returns 200 with correct data
    """
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url, {'org_id': 'orHVw3ikkCxJ'})
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert dict_compare_keys(response_data, fixture['orgs']) == [], 'orgs GET diff in keys'


def test_orgs_get_view_case_2(mock_dependencies, api_client, access_token):
    """
    Test orgs GET view
    Case: Invalid org_id returns 404
    """
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url, {'org_id': 'wrong_org_id'})
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response_data = json.loads(response.content)
    assert response_data['message'] is not None


def test_orgs_put_view_case_1(mock_dependencies, api_client, access_token):
    """
    Test orgs PUT view
    Case: Returns 200 for partner orgs
    """
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.put(url)
    assert response.status_code == status.HTTP_200_OK


def test_new_org_put_view_case_1(mock_dependencies, api_client, mocker, access_token):
    """
    Test new org PUT view
    Case: Returns 200 for new partner org
    """
    mock_get_fyle_admin(mocker)

    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.put(url)
    assert response.status_code == status.HTTP_200_OK


def test_admin_view_case_1(mock_dependencies, api_client, mocker, access_token, create_org):
    """
    Test admin view
    Case: Returns 200 with employee data
    """
    url = reverse('admin-view', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    mock_platform_employees_list(mocker)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [{"email": "abc@ac.com", "name": "abc"}]
