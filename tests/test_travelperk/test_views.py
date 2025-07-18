import json
import pytest
from django.urls import reverse
from rest_framework import status

from apps.integrations.models import Integration
from apps.orgs.models import Org
from apps.travelperk.actions import add_travelperk_to_integrations
from apps.travelperk.models import TravelperkAdvancedSetting, TravelPerk, TravelperkCredential
from tests.helper import dict_compare_keys
from .fixtures import fixture, webhook_data_valid, webhook_data_invalid, connect_travelperk_data, integration_test_data, test_signature, test_integration_tpa_name, test_integration_tpa_id, test_integration_type
from .mock_setup import (
    mock_platform_connector,
    mock_travelperk_connector_disconnect,
    mock_travelperk_connector_connect,
    mock_get_refresh_token,
    mock_test_disconnect_travelperk_case_2,
    mock_test_connect_travelperk_case_2,
    mock_test_webhook_case_1,
    mock_test_sync_payment_profiles_case_1,
    mock_test_validate_healthy_token_case_1
)


def test_travelperk_get_view_case_1(mock_dependencies, api_client, access_token, create_travelperk_full_setup):
    """
    Test travelperk GET view
    Case: Valid org_id returns 200 with correct data
    """
    setup = create_travelperk_full_setup
    url = reverse('travelperk:travelperk', kwargs={'org_id': setup['org'].id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert dict_compare_keys(response_data, fixture['travelperk']) == [], 'travelperk GET diff in keys'


def test_travelperk_get_view_case_2(mock_dependencies, api_client, access_token):
    """
    Test travelperk GET view
    Case: Invalid org_id returns 404
    """
    url = reverse('travelperk:travelperk', kwargs={'org_id': 123})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response_data = json.loads(response.content)
    assert response_data['message'] is not None


def test_get_profile_mappings_case_1(mock_dependencies, api_client, access_token, create_org, create_travelperk):
    """
    Test get profile mappings
    Case: POST and GET operations work correctly
    """
    url = reverse('travelperk:profile-mappings', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, mock_dependencies.profile_mapping_payload, format='json')
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert response_data[0]['profile_name'] == 'Dummy Profile'

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert response_data['results'][0]['profile_name'] == 'Dummy Profile'


def test_get_advanced_settings_case_1(mock_dependencies, api_client, access_token, create_travelperk_full_setup):
    """
    Test get advanced settings
    Case: POST creates integration and GET returns user data
    """
    setup = create_travelperk_full_setup
    url = reverse('travelperk:advance-settings-view', kwargs={'org_id': setup['org'].id})

    travelperk = setup['travelperk']
    travelperk.onboarding_state = 'ADVANCED_SETTINGS'
    travelperk.save()

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    payload = mock_dependencies.advance_setting_payload
    payload['org'] = setup['org'].id

    response = api_client.post(url, payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    integration_object = Integration.objects.get(org_id=setup['org'].fyle_org_id, type='TRAVEL')
    assert integration_object is not None
    assert integration_object.tpa_name == mock_dependencies.integrations_response['tpa_name']
    assert integration_object.tpa_id == mock_dependencies.integrations_response['tpa_id']
    assert integration_object.type == mock_dependencies.integrations_response['type']
    assert integration_object.org_id == setup['org'].fyle_org_id
    assert integration_object.org_name == setup['org'].name
    assert integration_object.is_active is True
    assert integration_object.is_beta is True

    advanced_settings = TravelperkAdvancedSetting.objects.get(org=setup['org'].id)
    advanced_settings.default_employee_name = None
    advanced_settings.default_employee_id = None
    advanced_settings.save()

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert response_data['default_employee_name'] == 'ashwin.t@fyle.in'
    assert response_data['default_employee_id'] == 'usqywo0f3nBY'


def test_disconnect_travelperk_case_1(mock_dependencies, api_client, mocker, access_token, create_travelperk_full_setup):
    """
    Test disconnect travelperk
    Case: Valid disconnect call returns 200 and updates integration
    """
    setup = create_travelperk_full_setup
    url = reverse('travelperk:disconnect-travelperk', kwargs={'org_id': setup['org'].id})

    add_travelperk_to_integrations(setup['org'].id)

    integration_objects = Integration.objects.filter(org_id=setup['org'].fyle_org_id, type='TRAVEL')
    assert integration_objects.count() == 1

    mock_travelperk_connector_disconnect(mocker)

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK

    integration_object = Integration.objects.get(org_id=setup['org'].fyle_org_id, type='TRAVEL')
    assert integration_object.is_active is False
    assert integration_object.disconnected_at is not None


@pytest.mark.shared_mocks(lambda mocker: mock_test_disconnect_travelperk_case_2(mocker))
def test_disconnect_travelperk_case_2(mock_dependencies, api_client, access_token, create_org):
    """
    Test disconnect travelperk
    Case: TravelPerk credentials not found returns 500
    """
    url = reverse('travelperk:disconnect-travelperk', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    response = api_client.post(url)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_connect_travelperk_case_1(mock_dependencies, api_client, mocker, access_token, create_travelperk_full_setup):
    """
    Test connect travelperk
    Case: Valid connect call returns 200
    """
    setup = create_travelperk_full_setup
    url = reverse('travelperk:connect-travelperk', kwargs={'org_id': setup['org'].id})

    mock_travelperk_connector_connect(mocker)
    mock_get_refresh_token(mocker)

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.shared_mocks(lambda mocker: mock_test_connect_travelperk_case_2(mocker))
def test_connect_travelperk_case_2(mock_dependencies, api_client, access_token, create_org):
    """
    Test connect travelperk
    Case: Exception during connection returns 400
    """
    url = reverse('travelperk:connect-travelperk', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, connect_travelperk_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.shared_mocks(lambda mocker: mock_test_webhook_case_1(mocker))
def test_webhook_case_1(mock_dependencies, api_client, create_org):
    """
    Test webhook endpoint
    Case: Valid webhook data creates expenses
    """
    url = reverse('travelperk:travelperk-webhook', kwargs={'org_id': create_org.id})
    
    response = api_client.post(
        url, 
        webhook_data_valid, 
        format='json',
        HTTP_TK_WEBHOOK_HMAC_SHA256=test_signature
    )
    assert response.status_code == status.HTTP_200_OK


def test_webhook_case_2(mock_dependencies, api_client, create_org):
    """
    Test webhook endpoint
    Case: Missing signature header returns 500
    """
    url = reverse('travelperk:travelperk-webhook', kwargs={'org_id': create_org.id})
    
    response = api_client.post(url, webhook_data_invalid, format='json')
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.shared_mocks(lambda mocker: mock_test_sync_payment_profiles_case_1(mocker))
def test_sync_payment_profiles_case_1(mock_dependencies, api_client, access_token, create_travelperk_full_setup):
    """
    Test sync payment profiles
    Case: Successfully syncs profiles
    """
    setup = create_travelperk_full_setup
    url = reverse('travelperk:sync-payment-profiles', kwargs={'org_id': setup['org'].id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.shared_mocks(lambda mocker: mock_test_validate_healthy_token_case_1(mocker))
def test_validate_healthy_token_case_1(mock_dependencies, api_client, access_token, create_travelperk_full_setup):
    """
    Test validate healthy token
    Case: Returns token validation status
    """
    setup = create_travelperk_full_setup
    url = reverse('travelperk:token-health', kwargs={'org_id': setup['org'].id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
