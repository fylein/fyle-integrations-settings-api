import json
import pytest
from django.urls import reverse
from rest_framework import status
from .fixture import post_integration_accounting, post_integration_accounting_2, post_integration_hrms, patch_integration_no_tpa_name, patch_integration, patch_integration_invalid_tpa_name, patch_integration_partial, delete_integration, delete_integration_no_tpa_name

from apps.integrations.models import Integration
from .fixture import (
    post_integration_accounting,
    post_integration_accounting_2,
    post_integration_hrms,
    patch_integration_no_tpa_name,
    patch_integration,
    patch_integration_invalid_tpa_name,
    patch_integration_partial,
    inactive_integration_data
)
from tests.helper import dict_compare_keys


def test_integrations_view_post_accounting_case_1(mock_dependencies, api_client, mocker, access_token):
    """
    Test integrations view POST
    Case: Create accounting integration and verify response
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    expected_data = {
        'org_id': mock_dependencies.org_id,
        'tpa_id': post_integration_accounting['tpa_id'],
        'tpa_name': post_integration_accounting['tpa_name'],
        'type': post_integration_accounting['type'],
        'is_active': post_integration_accounting['is_active'],
        'is_beta': True,
        'disconnected_at': None,
        'id': response_data['id'],
        'org_name': response_data['org_name'],
        'errors_count': response_data['errors_count'],
        'unmapped_card_count': response_data['unmapped_card_count'],
        'is_token_expired': response_data['is_token_expired'],
        'connected_at': response_data['connected_at'],
        'updated_at': response_data['updated_at']
    }
    assert dict_compare_keys(response_data, expected_data) == [], 'Response data mismatch'

    api_client.post(url, post_integration_accounting_2)
    api_client.post(url, post_integration_hrms)

    response = api_client.get(url)
    response_data = json.loads(response.content)

    assert response_data[0]['type'] == 'ACCOUNTING'
    assert response_data[1]['type'] == 'HRMS'
    assert response_data[0]['updated_at'] < response_data[1]['updated_at']


def test_integrations_view_post_case_1(mock_dependencies, api_client, mocker, access_token):
    """
    Test integrations view POST
    Case: Create and update integrations
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    expected_data = {
        'org_id': mock_dependencies.org_id,
        'tpa_id': post_integration_accounting['tpa_id'],
        'tpa_name': post_integration_accounting['tpa_name'],
        'type': post_integration_accounting['type'],
        'is_active': post_integration_accounting['is_active'],
        'is_beta': True,
        'disconnected_at': None,
        'id': response_data['id'],
        'org_name': response_data['org_name'],
        'errors_count': response_data['errors_count'],
        'unmapped_card_count': response_data['unmapped_card_count'],
        'is_token_expired': response_data['is_token_expired'],
        'connected_at': response_data['connected_at'],
        'updated_at': response_data['updated_at']
    }
    assert dict_compare_keys(response_data, expected_data) == [], 'Response data mismatch'

    accounting_integration_id = response_data['id']

    response = api_client.post(url, post_integration_hrms)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    expected_data = {
        'org_id': mock_dependencies.org_id,
        'tpa_id': post_integration_hrms['tpa_id'],
        'tpa_name': post_integration_hrms['tpa_name'],
        'type': post_integration_hrms['type'],
        'is_active': post_integration_hrms['is_active'],
        'is_beta': True,
        'disconnected_at': None,
        'id': response_data['id'],
        'org_name': response_data['org_name'],
        'errors_count': response_data['errors_count'],
        'unmapped_card_count': response_data['unmapped_card_count'],
        'is_token_expired': response_data['is_token_expired'],
        'connected_at': response_data['connected_at'],
        'updated_at': response_data['updated_at']
    }
    assert dict_compare_keys(response_data, expected_data) == [], 'Response data mismatch'

    response = api_client.post(url, post_integration_accounting_2)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    assert response_data['id'] == accounting_integration_id
    assert Integration.objects.filter(org_id=mock_dependencies.org_id).count() == 2

    expected_data = {
        'org_id': mock_dependencies.org_id,
        'tpa_id': post_integration_accounting_2['tpa_id'],
        'tpa_name': post_integration_accounting_2['tpa_name'],
        'type': post_integration_accounting_2['type'],
        'is_active': post_integration_accounting_2['is_active'],
        'is_beta': True,
        'disconnected_at': None,
        'id': response_data['id'],
        'org_name': response_data['org_name'],
        'errors_count': response_data['errors_count'],
        'unmapped_card_count': response_data['unmapped_card_count'],
        'is_token_expired': response_data['is_token_expired'],
        'connected_at': response_data['connected_at'],
        'updated_at': response_data['updated_at']
    }
    assert dict_compare_keys(response_data, expected_data) == [], 'Response data mismatch'


def test_integrations_view_get_case_1(mock_dependencies, api_client, mocker, access_token, create_integrations):
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
    expected_data = {
        'org_id': mock_dependencies.org_id,
        'tpa_id': post_integration_accounting['tpa_id'],
        'tpa_name': post_integration_accounting['tpa_name'],
        'type': post_integration_accounting['type'],
        'is_active': post_integration_accounting['is_active'],
        'is_beta': True,
        'disconnected_at': None,
        'id': response_data[0]['id'],
        'org_name': response_data[0]['org_name'],
        'errors_count': response_data[0]['errors_count'],
        'unmapped_card_count': response_data[0]['unmapped_card_count'],
        'is_token_expired': response_data[0]['is_token_expired'],
        'connected_at': response_data[0]['connected_at'],
        'updated_at': response_data[0]['updated_at']
    }
    assert dict_compare_keys(response_data[0], expected_data) == [], 'Response data mismatch'

    response = api_client.get(url, {'type': 'HRMS'})
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert len(response_data) == 1
    expected_data = {
        'org_id': mock_dependencies.org_id,
        'tpa_id': post_integration_hrms['tpa_id'],
        'tpa_name': post_integration_hrms['tpa_name'],
        'type': post_integration_hrms['type'],
        'is_active': post_integration_hrms['is_active'],
        'is_beta': True,
        'disconnected_at': None,
        'id': response_data[0]['id'],
        'org_name': response_data[0]['org_name'],
        'errors_count': response_data[0]['errors_count'],
        'unmapped_card_count': response_data[0]['unmapped_card_count'],
        'is_token_expired': response_data[0]['is_token_expired'],
        'connected_at': response_data[0]['connected_at'],
        'updated_at': response_data[0]['updated_at']
    }
    assert dict_compare_keys(response_data[0], expected_data) == [], 'Response data mismatch'


def test_integrations_view_invalid_access_token_case_1(mock_dependencies, api_client):
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

    response = api_client.delete(url, json.dumps(delete_integration), content_type="application/json")
    assert response.status_code == 403


def test_integrations_view_mark_inactive_post_case_1(mock_dependencies, api_client, mocker, access_token, create_integrations):
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

    inactive_data = {
        'id': integration_id,
        **inactive_integration_data
    }

    response = api_client.patch(url, inactive_data, format='json')
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert response_data['is_active'] is False


def test_integrations_view_patch_case_1(mock_dependencies, api_client, mocker, access_token):
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
    expected_data = {
        'id': integration_id,
        'org_id': mock_dependencies.org_id,
        'tpa_name': patch_integration['tpa_name'],
        'errors_count': patch_integration['errors_count'],
        'unmapped_card_count': patch_integration['unmapped_card_count'],
        'is_token_expired': patch_integration['is_token_expired'],
        'is_beta': True,
        'disconnected_at': None,
        'org_name': response_data['org_name'],
        'tpa_id': response_data['tpa_id'],
        'type': response_data['type'],
        'is_active': response_data['is_active'],
        'connected_at': response_data['connected_at'],
        'updated_at': response_data['updated_at']
    }
    assert dict_compare_keys(response_data, expected_data) == [], 'Response data mismatch'


def test_integrations_view_patch_case_2(mock_dependencies, api_client, mocker, access_token):
    """
    Test integrations view PATCH
    Case: Update integration with invalid tpa_name
    """
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == status.HTTP_201_CREATED

    patch_data = {
        'tpa_name': post_integration_accounting['tpa_name'],  # Use the same tpa_name
        'errors_count': 12,
        'unmapped_card_count': 10,
        'is_token_expired': False
    }
    
    response = api_client.patch(url, patch_data, format='json')
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    
    assert response_data['tpa_name'] == patch_data['tpa_name']
    assert response_data['errors_count'] == patch_data['errors_count']
    assert response_data['unmapped_card_count'] == patch_data['unmapped_card_count']
    assert response_data['is_token_expired'] == patch_data['is_token_expired']


def test_integrations_view_patch_case_3(mock_dependencies, api_client, mocker, access_token):
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
    assert response_data['is_beta'] is True
    assert response_data['disconnected_at'] is None
    
    assert response_data['tpa_name'] == patch_integration_partial['tpa_name']
    assert response_data['is_token_expired'] == patch_integration_partial['is_token_expired']
    
    assert 'errors_count' in response_data
    assert response_data['errors_count'] == 0

    assert 'unmapped_card_count' in response_data
    assert response_data['unmapped_card_count'] == 0


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_delete(api_client, mocker, access_token):
    """
    Test the DELETE API of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )

    integration = Integration.objects.create(
        org_id=dummy_org_id,
        tpa_name=delete_integration['tpa_name'],
        tpa_id='tpa129sjcjkjx',
        type='ACCOUNTING',
        is_active=True
    )

    assert Integration.objects.filter(id=integration.id).exists()

    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.delete(url, json.dumps(delete_integration_no_tpa_name), content_type="application/json")
    assert response.status_code == 400, 'DELETE without a tpa_name should return 400'

    api_client.credentials(HTTP_AUTHORIZATION='')
    response = api_client.delete(url, json.dumps(delete_integration), content_type="application/json")
    assert response.status_code == 401, 'DELETE with invalid access token should return 401'

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    response = api_client.delete(url, json.dumps(delete_integration), content_type="application/json")
    assert response.status_code == 204, 'Valid DELETE request should return 204'

    assert not Integration.objects.filter(id=integration.id).exists(), 'Integration should be deleted'

    response = api_client.delete(url, json.dumps(delete_integration), content_type="application/json")
    assert response.status_code == 400, 'DELETE on non-existent integration should return 400'


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_delete_exception(api_client, mocker, access_token):
    """
    Test the DELETE API of Integrations when super().delete() throws an exception
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )

    Integration.objects.create(
        org_id=dummy_org_id,
        tpa_name=delete_integration['tpa_name'],
        tpa_id='tpa129sjcjkjx',
        type='ACCOUNTING',
        is_active=True
    )

    mocker.patch(
        'apps.integrations.views.generics.DestroyAPIView.delete',
        side_effect=Exception('Database error')
    )

    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.delete(url, json.dumps(delete_integration), content_type="application/json")
    assert response.status_code == 500, 'DELETE with exception should return 500'
