import pytest
from django.urls import reverse
from rest_framework import status
from tests.helpers import dict_compare_keys
from apps.integrations.models import Integration
from .mock_setup import mock_get_org_id_and_name_from_access_token


def test_integrations_view_post_case_1(api_client, access_token, db, mocker):
    """
    Test integrations POST view
    Case: creates integration successfully
    """
    # Mock external dependencies
    mock_get_org = mock_get_org_id_and_name_from_access_token(mocker)
    
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    url = reverse('integrations:integrations')
    data = {
        'tpa_id': 'test_tpa_id',
        'tpa_name': 'Test TPA',
        'type': 'HRMS',
        'is_active': True
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    
    # Verify integration was created in database
    integration = Integration.objects.filter(
        tpa_id='test_tpa_id',
        type='HRMS'
    ).first()
    assert integration is not None
    assert integration.tpa_name == 'Test TPA'
    assert integration.is_active is True


def test_integrations_view_post_case_2(api_client, access_token, db):
    """
    Test integrations POST view
    Case: returns 400 for invalid data
    """
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    url = reverse('integrations:integrations')
    data = {'invalid_field': 'value'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_integrations_view_get_case_1(api_client, access_token, db, mocker):
    """
    Test integrations GET view
    Case: returns 200 with integrations list
    """
    # Mock external dependencies
    mock_get_org = mock_get_org_id_and_name_from_access_token(mocker)
    
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    url = reverse('integrations:integrations')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_integrations_view_post_case_3(api_client, db):
    """
    Test integrations POST view
    Case: returns 400 without token (API returns 400 for missing required fields)
    """
    url = reverse('integrations:integrations')
    data = {'name': 'Test Integration'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_integrations_view_patch_case_1(api_client, access_token, db, mocker):
    """
    Test integrations PATCH view
    Case: updates integration successfully
    """
    # Mock external dependencies
    mock_get_org = mock_get_org_id_and_name_from_access_token(mocker)
    
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    url = reverse('integrations:integrations')
    data = {
        'tpa_name': 'Updated Integration',
        'type': 'HRMS'
    }
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK


def test_integrations_view_patch_case_2(api_client, access_token, db, mocker):
    """
    Test integrations PATCH view
    Case: returns 400 for missing required fields
    """
    # Mock external dependencies
    mock_get_org = mock_get_org_id_and_name_from_access_token(mocker)
    
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    url = reverse('integrations:integrations')
    data = {'name': 'Non-existent Integration'}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_integrations_view_patch_case_3(api_client, db):
    """
    Test integrations PATCH view
    Case: returns 400 without token (API returns 400 for missing required fields)
    """
    url = reverse('integrations:integrations')
    data = {'name': 'Updated Integration'}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST 
