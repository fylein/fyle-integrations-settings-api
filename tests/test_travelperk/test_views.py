
import json
import pytest
from django.urls import reverse
from unittest.mock import MagicMock

from apps.integrations.models import Integration
from apps.orgs.models import Org
from apps.travelperk.actions import add_travelperk_to_integrations
from apps.travelperk.models import TravelperkAdvancedSetting
from tests.helper import dict_compare_keys
from .fixtures import fixture

@pytest.mark.django_db(databases=['default'])
def test_travelperk_get_view(api_client, access_token, get_org_id, get_travelperk_id):
    """
    Test Get of Travelperk
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


@pytest.mark.django_db(databases=['default'])
def test_get_profile_mappings(api_client, access_token, get_org_id, get_travelperk_id):
    """
    Test Get of Travelperk
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


@pytest.mark.django_db(databases=['default'])
def test_get_advanced_settings(mocker, api_client, access_token, get_org_id, get_travelperk):
    """
    Test Get of Travelperk
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

    advanced_settings = TravelperkAdvancedSetting.objects.get(org=get_org_id)
    advanced_settings.default_employee_name = None
    advanced_settings.default_employee_id = None
    advanced_settings.save()

    mock_connector = MagicMock()
    mock_connector.connection.v1.spender.my_profile.get.return_value = {'data': {'user': {'email': 'janedoe@gmail.com', 'id': '1234'}}}

    mocker.patch(
        'apps.travelperk.views.PlatformConnector',
        return_value=mock_connector
    )

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert response['default_employee_name'] == 'janedoe@gmail.com'
    assert response['default_employee_id'] == '1234'


@pytest.mark.django_db(databases=['default'])
def test_disconnect_travelperk(mocker, api_client, access_token, get_org_id, get_travelperk_id, add_travelperk_cred):
    """
    Test Disconnect Travelperk
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

    mock_connector = MagicMock()
    mock_connector.delete_webhook_connection.return_value = {'message': 'success'}

    mocker.patch(
        'apps.travelperk.views.TravelperkConnector',
        return_value=mock_connector
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Disconnect call should return 200 and update the integration instance
    response = api_client.post(url)
    assert response.status_code == 200

    integration_object = Integration.objects.get(org_id=org.fyle_org_id, type='TRAVEL')
    assert not integration_object.is_active
    assert integration_object.disconnected_at is not None

@pytest.mark.django_db(databases=['default'])
def test_connect_travelperk(mocker, api_client, access_token, get_org_id, get_travelperk_id, add_travelperk_cred):
    """
    Test Connect Travelperk
    """

    url = reverse('travelperk:connect-travelperk',
        kwargs={
                'org_id': get_org_id,
            }
    )

    mock_connector = MagicMock()
    mock_connector.create_webhook.return_value = {'id': 123}

    mocker.patch(
        'apps.travelperk.views.TravelperkConnector',
        return_value=mock_connector
    )

    mocker.patch(
        'apps.travelperk.views.get_refresh_token_using_auth_code',
        return_value={'123e3rwer'}
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url)

    assert response.status_code == 200

    response = json.loads(response.content)
    assert response['id'] == 123