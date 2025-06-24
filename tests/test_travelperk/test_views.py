import json
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.integrations.models import Integration
from apps.orgs.models import Org, FyleCredential
from apps.travelperk.actions import add_travelperk_to_integrations
from apps.travelperk.models import TravelperkAdvancedSetting, TravelPerk, TravelperkCredential
from tests.helper import dict_compare_keys
from .fixtures import fixture
from .mock_setup import (
    mock_platform_connector,
    mock_travelperk_connector,
    mock_get_refresh_token,
    mock_org_get_exception,
    mock_profile_mapping_exception,
    mock_platform_connector_with_profile,
    mock_travelperk_get_exception,
    mock_travelperk_connector_with_validation
)

def test_travelperk_get_view_case_1(api_client, access_token, get_org_id, get_travelperk_id, db):
    """
    Test travelperk GET view
    Case: returns 200 for valid org_id and 404 for invalid org_id
    """
    url = reverse('travelperk:travelperk',
        kwargs={
                'org_id': get_org_id,
            }
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['travelperk']) == [], 'orgs GET diff in keys'

    url = reverse('travelperk:travelperk',
        kwargs={
                'org_id': 123,
            }
    )
    response = api_client.get(url)
    assert response.status_code == 404

    response = json.loads(response.content)
    assert response['message'] != None


def test_get_profile_mappings_case_1(api_client, access_token, get_org_id, get_travelperk_id, db):
    """
    Test profile mappings view
    Case: creates and retrieves profile mapping successfully
    """
    url = reverse('travelperk:profile-mappings',
        kwargs={
                'org_id': get_org_id,
            }
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    payload = [
            {
                "profile_name": 'Dummy Profile',
                "is_import_enabled": False,
                "user_role": "CARD_HOLDER"
            }
        ]

    response = api_client.post(url, payload, format='json')
    assert response.status_code == 200

    response = json.loads(response.content)
    assert response[0]['profile_name'] == 'Dummy Profile'

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert response['results'][0]['profile_name'] == 'Dummy Profile'
    assert dict_compare_keys(response['results'][0], fixture['profile_mapping']['results'][0]) == []


def test_get_advanced_settings_case_1(mocker, api_client, access_token, get_org_id, get_travelperk, db):
    """
    Test advanced settings view
    Case: creates advanced settings and integration, then retrieves with default values
    """
    url = reverse('travelperk:advance-settings-view',
        kwargs={
                'org_id': get_org_id,
            }
    )

    travelperk = get_travelperk
    travelperk.onboarding_state = 'ADVANCED_SETTINGS'
    travelperk.save()

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    payload = fixture['advance_setting_payload']
    payload['org'] = get_org_id

    response = api_client.post(url, payload, format='json')
    assert response.status_code == 201

    # Verify integration was created in database
    org = Org.objects.get(id=get_org_id)
    integration_object = Integration.objects.get(org_id=org.fyle_org_id, type='TRAVEL')
    assert integration_object
    assert integration_object.tpa_name == fixture['integrations_response']['tpa_name']
    assert integration_object.tpa_id == fixture['integrations_response']['tpa_id']
    assert integration_object.type == fixture['integrations_response']['type']
    assert integration_object.org_id == org.fyle_org_id
    assert integration_object.org_name == org.name
    assert integration_object.is_active
    assert integration_object.is_beta

    # Verify advanced settings were created
    advanced_settings = TravelperkAdvancedSetting.objects.get(org=get_org_id)
    advanced_settings.default_employee_name = None
    advanced_settings.default_employee_id = None
    advanced_settings.save()

    mock_platform = mock_platform_connector(mocker)

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert response['default_employee_name'] == 'janedoe@gmail.com'
    assert response['default_employee_id'] == '1234'


def test_disconnect_travelperk_case_1(mocker, api_client, access_token, get_org_id, get_travelperk_id, add_travelperk_cred, db):
    """
    Test disconnect travelperk view
    Case: disconnects travelperk integration successfully
    """
    url = reverse('travelperk:disconnect-travelperk',
        kwargs={
                'org_id': get_org_id,
            }
    )

    # Create mock travelperk integration record
    add_travelperk_to_integrations(get_org_id)

    org = Org.objects.get(id=get_org_id)
    integration_objects = Integration.objects.filter(org_id=org.fyle_org_id, type='TRAVEL')
    assert integration_objects.count() == 1

    mock_travelperk = mock_travelperk_connector(mocker)

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Disconnect call should return 200 and update the integration instance
    response = api_client.post(url)
    assert response.status_code == 200

    # Verify integration was deactivated in database
    integration_object = Integration.objects.get(org_id=org.fyle_org_id, type='TRAVEL')
    assert not integration_object.is_active
    assert integration_object.disconnected_at is not None

def test_connect_travelperk_case_1(mocker, api_client, access_token, get_org_id, get_travelperk_id, add_travelperk_cred, db):
    """
    Test connect travelperk view
    Case: connects travelperk integration successfully
    """
    url = reverse('travelperk:connect-travelperk',
        kwargs={
                'org_id': get_org_id,
            }
    )

    mock_travelperk = mock_travelperk_connector(mocker)
    mock_token = mock_get_refresh_token(mocker)

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url)

    assert response.status_code == 200

    response = json.loads(response.content)
    assert response['id'] == 123

def test_connect_travelperk_error_case_1(mocker, api_client, access_token, get_org_id, db):
    """
    Test connect travelperk view
    Case: error during connection (Org.objects.get raises exception)
    """
    url = reverse('travelperk:connect-travelperk', kwargs={'org_id': get_org_id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Use shared mock for Org.objects.get exception
    mock_org_get_exception(mocker)
    response = api_client.post(url, {'code': 'dummy'}, format='json')
    assert response.status_code == 400  # View returns 400 for exceptions

def test_travelperk_webhook_invalid_signature_case_1(api_client, get_org_id, db):
    """
    Test travelperk webhook with invalid signature
    Case: returns 400 for invalid signature
    """
    url = reverse('travelperk:travelperk-webhook', kwargs={'org_id': get_org_id})
    
    # Add the required header with invalid signature
    headers = {'HTTP_TK_WEBHOOK_HMAC_SHA256': 'invalid_signature'}
    response = api_client.post(url, {'data': 'test'}, format='json', **headers)
    assert response.status_code == 400

def test_profile_mappings_error_case_1(mocker, api_client, access_token, get_org_id, db):
    """
    Test profile mappings error handling
    Case: handles exception during profile mapping creation
    """
    url = reverse('travelperk:profile-mappings', kwargs={'org_id': get_org_id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    payload = [{"profile_name": 'Dummy Profile', "is_import_enabled": False, "user_role": "CARD_HOLDER"}]
    
    # Use shared mock for profile mapping exception
    mock_profile_mapping_exception(mocker)
    
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 500

def test_advanced_settings_get_object_sets_defaults_case_1(mocker, api_client, access_token, get_org_id, db):
    """
    Test advanced settings get object sets defaults
    Case: sets default values when advanced settings don't exist
    """
    url = reverse('travelperk:advance-settings-view', kwargs={'org_id': get_org_id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    # Use shared mock for platform connector with profile
    mock_platform = mock_platform_connector_with_profile(mocker)
    
    response = api_client.get(url)
    assert response.status_code == 200
    
    response = json.loads(response.content)
    assert response['default_employee_name'] == 'janedoe@gmail.com'
    assert response['default_employee_id'] == '1234'

def test_validate_healthy_token_not_found_case_1(mocker, api_client, access_token, get_org_id, db):
    """
    Test validate healthy token not found
    Case: handles TravelPerk.objects.get exception
    """
    url = reverse('travelperk:token-health', kwargs={'org_id': get_org_id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Use shared mock for TravelPerk.objects.get exception
    mock_travelperk_get_exception(mocker)

    response = api_client.get(url)
    assert response.status_code == 400  # View returns 400 for exceptions

def test_validate_healthy_token_expired_case_1(mocker, api_client, access_token, get_org_id, db):
    """
    Test validate healthy token expired
    Case: handles expired token validation
    """
    url = reverse('travelperk:token-health', kwargs={'org_id': get_org_id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Create required objects first
    from apps.orgs.models import Org
    from apps.travelperk.models import TravelPerk, TravelperkCredential
    
    org, created = Org.objects.get_or_create(
        id=get_org_id, 
        defaults={'name': 'Test Org', 'fyle_org_id': 'test_org_id'}
    )
    travelperk = TravelPerk.objects.create(org=org, is_travelperk_connected=True)
    travelperk_credential = TravelperkCredential.objects.create(org=org)

    # Use shared mock for travelperk connector with validation
    mock_connector = mock_travelperk_connector_with_validation(mocker)

    response = api_client.get(url)
    assert response.status_code == 400  # View returns 400 for expired tokens
