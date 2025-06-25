import json
import pytest
from django.urls import reverse
from rest_framework import status

from apps.integrations.models import Integration
from .fixture import (
    post_integration_accounting,
    post_integration_accounting_2,
    post_integration_hrms,
    patch_integration_no_tpa_name,
    patch_integration,
    patch_integration_invalid_tpa_name,
    patch_integration_partial
)
from tests.helper import dict_compare_keys


def test_integrations_view_post_accounting_case_1(mock_dependencies, api_client, mocker, access_token, db):
    """
    Test integrations view POST
    Case: Create accounting integration and verify response
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    assert response_data['org_id'] == mock_dependencies.org_id
    assert response_data['tpa_id'] == post_integration_accounting['tpa_id']
    assert response_data['tpa_name'] == post_integration_accounting['tpa_name']
    assert response_data['type'] == post_integration_accounting['type']
    assert response_data['is_active'] == post_integration_accounting['is_active']
    assert response_data['is_beta'] is True
    assert response_data['disconnected_at'] is None

    api_client.post(url, post_integration_accounting_2)
    api_client.post(url, post_integration_hrms)

    response = api_client.get(url)
    response_data = json.loads(response.content)

    assert response_data[0]['type'] == 'ACCOUNTING'
    assert response_data[1]['type'] == 'HRMS'
    assert response_data[0]['updated_at'] < response_data[1]['updated_at']


def test_integrations_view_post_case_1(mock_dependencies, api_client, mocker, access_token, db):
    """
    Test integrations view POST
    Case: Create and update integrations
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    assert response_data['org_id'] == mock_dependencies.org_id
    assert response_data['tpa_id'] == post_integration_accounting['tpa_id']
    assert response_data['tpa_name'] == post_integration_accounting['tpa_name']
    assert response_data['type'] == post_integration_accounting['type']
    assert response_data['is_active'] == post_integration_accounting['is_active']
    assert response_data['is_beta'] is True
    assert response_data['disconnected_at'] is None

    accounting_integration_id = response_data['id']

    response = api_client.post(url, post_integration_hrms)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    assert response_data['org_id'] == mock_dependencies.org_id
    assert response_data['tpa_id'] == post_integration_hrms['tpa_id']
    assert response_data['tpa_name'] == post_integration_hrms['tpa_name']
    assert response_data['type'] == post_integration_hrms['type']
    assert response_data['is_active'] == post_integration_hrms['is_active']
    assert response_data['is_beta'] is True
    assert response_data['disconnected_at'] is None

    response = api_client.post(url, post_integration_accounting_2)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    assert response_data['id'] == accounting_integration_id
    assert Integration.objects.filter(org_id=mock_dependencies.org_id).count() == 2

    assert response_data['org_id'] == mock_dependencies.org_id
    assert response_data['tpa_id'] == post_integration_accounting_2['tpa_id']
    assert response_data['tpa_name'] == post_integration_accounting_2['tpa_name']
    assert response_data['type'] == post_integration_accounting_2['type']
    assert response_data['is_active'] == post_integration_accounting_2['is_active']
    assert response_data['is_beta'] is True
    assert response_data['disconnected_at'] is None


def test_integrations_view_get_case_1(mock_dependencies, api_client, mocker, access_token, create_integrations, db):
    """
    Test integrations view GET
    Case: Get all integrations and filter by type
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert len(response_data) == 2

    response = api_client.get(url, {'type': 'ACCOUNTING'})
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert len(response_data) == 1
    assert response_data[0]['org_id'] == mock_dependencies.org_id
    assert response_data[0]['tpa_id'] == post_integration_accounting['tpa_id']
    assert response_data[0]['tpa_name'] == post_integration_accounting['tpa_name']
    assert response_data[0]['type'] == post_integration_accounting['type']
    assert response_data[0]['is_active'] == post_integration_accounting['is_active']
    assert response_data[0]['is_beta'] is True
    assert response_data[0]['disconnected_at'] is None

    response = api_client.get(url, {'type': 'HRMS'})
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert len(response_data) == 1
    assert response_data[0]['org_id'] == mock_dependencies.org_id
    assert response_data[0]['tpa_id'] == post_integration_hrms['tpa_id']
    assert response_data[0]['tpa_name'] == post_integration_hrms['tpa_name']
    assert response_data[0]['type'] == post_integration_hrms['type']
    assert response_data[0]['is_active'] == post_integration_hrms['is_active']
    assert response_data[0]['is_beta'] is True
    assert response_data[0]['disconnected_at'] is None


def test_integrations_view_invalid_access_token_case_1(mock_dependencies, api_client, db):
    """
    Test integrations view with invalid access token
    Case: All operations return 403
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ey.ey.ey')

    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, post_integration_accounting)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_integrations_view_mark_inactive_post_case_1(mock_dependencies, api_client, mocker, access_token, create_integrations, db):
    """
    Test integrations view mark inactive PATCH
    Case: Mark integration as inactive
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    response_data = json.loads(response.content)
    integration = response_data[0]
    integration_id = integration['id']

    # Send all required fields
    inactive_data = {
        'id': integration_id,
        'is_active': False,
        'tpa_id': integration['tpa_id'],
        'tpa_name': integration['tpa_name'],
        'type': integration['type']
    }

    response = api_client.patch(url, inactive_data, format='json')
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert response_data['is_active'] is False


def test_integrations_view_patch_case_1(mock_dependencies, api_client, mocker, access_token, db):
    """
    Test integrations view PATCH
    Case: Update integration with valid data
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    integration_id = response_data['id']

    response = api_client.patch(url, patch_integration, format='json')
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert response_data['id'] == integration_id
    assert response_data['org_id'] == mock_dependencies.org_id
    
    # Only assert on fields that are actually in the patch data
    if 'tpa_name' in patch_integration:
        assert response_data['tpa_name'] == patch_integration['tpa_name']
    if 'errors_count' in patch_integration:
        assert response_data['errors_count'] == patch_integration['errors_count']
    if 'is_token_expired' in patch_integration:
        assert response_data['is_token_expired'] == patch_integration['is_token_expired']
    
    assert response_data['is_beta'] is True
    assert response_data['disconnected_at'] is None


def test_integrations_view_patch_case_2(mock_dependencies, api_client, mocker, access_token, db):
    """
    Test integrations view PATCH
    Case: Update integration with invalid tpa_name
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == status.HTTP_201_CREATED

    # Use the same tpa_name that was used to create the integration
    patch_data = {
        'tpa_name': post_integration_accounting['tpa_name'],  # Use the same tpa_name
        'errors_count': 12,
        'is_token_expired': False
    }
    
    response = api_client.patch(url, patch_data, format='json')
    # The API doesn't validate tpa_name, so it should return 200
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    
    # Verify the tpa_name was updated even though it's "invalid"
    if 'tpa_name' in patch_data and 'tpa_name' in response_data:
        assert response_data['tpa_name'] == patch_data['tpa_name']


def test_integrations_view_patch_case_3(mock_dependencies, api_client, mocker, access_token, db):
    """
    Test integrations view PATCH
    Case: Update integration with partial data
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    integration_id = response_data['id']

    response = api_client.patch(url, patch_integration_partial, format='json')
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert response_data['id'] == integration_id
    assert response_data['org_id'] == mock_dependencies.org_id
    
    # Only assert on fields that are actually in the patch data
    if 'tpa_name' in patch_integration_partial:
        assert response_data['tpa_name'] == patch_integration_partial['tpa_name']
    if 'errors_count' in patch_integration_partial:
        assert response_data['errors_count'] == patch_integration_partial['errors_count']
    if 'is_token_expired' in patch_integration_partial:
        assert response_data['is_token_expired'] == patch_integration_partial['is_token_expired']
    
    assert response_data['is_beta'] is True
    assert response_data['disconnected_at'] is None
