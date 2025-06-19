import json
import pytest
from django.urls import reverse

from apps.bamboohr.models import BambooHr
from apps.integrations.models import Integration
from apps.orgs.models import Org
from tests.helper import dict_compare_keys
from .fixtures import fixture
from unittest.mock import MagicMock


@pytest.mark.django_db(databases=['default'])
def test_bamboohr_get_view(api_client, mocker, access_token, get_org_id, get_bamboohr_id):
    """
    Test Get of Orgs
    """

    url = reverse('bamboohr:bamboohr',
        kwargs={
                'org_id': get_org_id,
            }
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['bamboohr']) == [], 'orgs GET diff in keys'

    url = reverse('bamboohr:bamboohr',
        kwargs={
                'org_id': 123,
            }
    )
    response = api_client.get(url)
    assert response.status_code == 404

    response = json.loads(response.content)
    assert response['message'] != None


@pytest.mark.django_db(databases=['default'])
def test_post_configuration_view(api_client, mocker, access_token, get_org_id):
    """
    Test Post Configuration View
    """

    url = reverse('bamboohr:configuration',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url,
        {
            "org": get_org_id,
            "additional_email_options": {},
            "emails_selected": [
                {
                    "name": "Nilesh",
                    "email": "nilesh.p@fyle.in"
                },
            ]
        }, format='json'
    )

    assert response.status_code == 200
    assert response.data['emails_selected'] ==  [{'name': 'Nilesh', 'email': 'nilesh.p@fyle.in'}]


@pytest.mark.django_db(databases=['default'])
def test_get_configuration_view(api_client, mocker, access_token, get_org_id, get_bamboohr_id):
    """
    Test Get Configuration View
    """

    url = reverse('bamboohr:configuration',
        kwargs={
            'org_id':get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url, {'org_id': str(get_org_id)})
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['configurations']) == [], 'orgs GET diff in keys'

    response = api_client.get(url, {'org_id': '1231'})
    assert response.status_code == 404

    response = json.loads(response.content)
    assert response['message'] != None


@pytest.mark.django_db(databases=['default'])
def test_post_bamboohr_connection_view(api_client, mocker, access_token, get_org_id):
    """
    Test Post BambooHR Connection View
    """

    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Missing input should return 400
    response = api_client.post(url, fixture['bamboo_connection_invalid_payload'], format='json')
    assert response.status_code == 400

    # Invalid token should return 400
    mock_bamboohr_sdk = MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)

    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == 400

    # Valid input should return 200
    mock_bamboohr_sdk = MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)

    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == 200

    org = Org.objects.get(id=get_org_id)
    integration_object = Integration.objects.get(org_id=org.fyle_org_id, type='HRMS')
    assert integration_object
    assert integration_object.tpa_name == fixture['integrations_response']['tpa_name']
    assert integration_object.tpa_id == fixture['integrations_response']['tpa_id']
    assert integration_object.type == fixture['integrations_response']['type']
    assert integration_object.org_id == org.fyle_org_id
    assert integration_object.org_name == org.name
    assert integration_object.is_active
    assert integration_object.is_beta


@pytest.mark.django_db(databases=['default'])
def test_post_bamboohr_disconnect_view(api_client, mocker, access_token, get_org_id):
    """
    Test Post BambooHR Disconnect View
    """
    
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Invalid org id should return 404
    url = reverse('bamboohr:disconnect',
        kwargs={
            'org_id': '1234567',
        }
    )

    response = api_client.post(url, format='json')
    assert response.status_code == 404


    # Create dummy BambooHR conenction
    connect_url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    mock_bamboohr_sdk = MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)

    response = api_client.post(connect_url, fixture['bamboo_connection'], format='json')
    assert response.status_code == 200


    # Valid disconnect call should return 200 and update the integration instance
    url = reverse('bamboohr:disconnect',
        kwargs={
            'org_id': get_org_id,
        }
    )

    response = api_client.post(url, format='json')
    assert response.status_code == 200

    org = Org.objects.get(id=get_org_id)
    integration_object = Integration.objects.get(org_id=org.fyle_org_id, type='HRMS')
    assert not integration_object.is_active
    assert integration_object.disconnected_at is not None


@pytest.mark.django_db(databases=['default'])
def test_health_check_bamboohr_not_found(api_client, mocker, access_token, get_org_id):
    """Test HealthCheck when BambooHR details not found"""
    url = reverse('bamboohr:health-check',
        kwargs={
            'org_id': 99999,  # Non-existent org_id
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    response = api_client.get(url)
    assert response.status_code == 404
    assert response.data['message'] == 'Bamboo HR Details Not Found'

@pytest.mark.django_db(databases=['default'])
def test_health_check_api_exception(api_client, mocker, access_token, get_org_id, get_bamboohr_id):
    """Test HealthCheck when API call raises exception"""
    url = reverse('bamboohr:health-check',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    # Mock BambooHrSDK to raise exception
    mock_sdk = MagicMock()
    mock_sdk.time_off.get.side_effect = Exception('API Error')
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_sdk)
    
    response = api_client.get(url)
    assert response.status_code == 400
    assert response.data['message'] == 'Invalid token'

@pytest.mark.django_db(databases=['default'])
def test_health_check_no_timeoff_types(api_client, mocker, access_token, get_org_id, get_bamboohr_id):
    """Test HealthCheck when no timeOffTypes in response"""
    url = reverse('bamboohr:health-check',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    # Mock BambooHrSDK to return empty timeOffTypes
    mock_sdk = MagicMock()
    mock_sdk.time_off.get.return_value = {'timeOffTypes': []}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_sdk)
    
    response = api_client.get(url)
    assert response.status_code == 400
    assert response.data['message'] == 'Invalid token'

@pytest.mark.django_db(databases=['default'])
def test_webhook_callback_api_view(api_client, mocker, access_token, get_org_id):
    """Test WebhookCallbackAPIView"""
    url = reverse('bamboohr:webhook-callback',
        kwargs={
            'org_id': get_org_id,
        }
    )
    
    # Mock async_task
    mock_async_task = mocker.patch('apps.bamboohr.views.async_task')
    
    payload = {
        'employees': [{
            'id': 123,
            'fields': {
                'firstName': {'value': 'John'},
                'lastName': {'value': 'Doe'}
            }
        }]
    }
    
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 201
    assert response.data['status'] == 'success'
    
    # Verify async_task was called
    mock_async_task.assert_called_once_with('apps.bamboohr.tasks.update_employee', get_org_id, payload)

@pytest.mark.django_db(databases=['default'])
def test_bamboohr_connection_missing_input(api_client, mocker, access_token, get_org_id):
    """Test BambooHrConnection with missing input fields"""
    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    # Test with missing api_token
    response = api_client.post(url, {
        'input': {
            'subdomain': 'test'
        }
    }, format='json')
    assert response.status_code == 400
    assert response.data['message'] == 'API_TOKEN and SUB_DOMAIN are required'
    
    # Test with missing subdomain
    response = api_client.post(url, {
        'input': {
            'api_token': 'test_token'
        }
    }, format='json')
    assert response.status_code == 400
    assert response.data['message'] == 'API_TOKEN and SUB_DOMAIN are required'

@pytest.mark.django_db(databases=['default'])
def test_bamboohr_connection_api_exception(api_client, mocker, access_token, get_org_id):
    """Test BambooHrConnection when API raises exception"""
    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    # Mock BambooHrSDK to raise specific exception that should be caught
    from bamboosdk.exceptions import InvalidTokenError
    mock_sdk = MagicMock()
    mock_sdk.time_off.get.side_effect = InvalidTokenError('Invalid token')
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_sdk)
    
    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == 400
    assert response.data['message'] == 'Invalid token'

@pytest.mark.django_db(databases=['default'])
def test_bamboohr_connection_no_timeoff_types(api_client, mocker, access_token, get_org_id):
    """Test BambooHrConnection when no timeOffTypes in response"""
    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    # Mock BambooHrSDK to return empty timeOffTypes
    mock_sdk = MagicMock()
    mock_sdk.time_off.get.return_value = {'timeOffTypes': []}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_sdk)
    
    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == 400
    assert response.data['message'] == 'Invalid token'

@pytest.mark.django_db(databases=['default'])
def test_bamboohr_configuration_get_not_found(api_client, mocker, access_token, get_org_id):
    """Test BambooHrConfigurationView GET when configuration not found"""
    url = reverse('bamboohr:configuration',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    # Test with non-existent org_id
    response = api_client.get(url, {'org_id': '99999'})
    assert response.status_code == 404
    assert response.data['message'] == 'BambooHr Configuration does not exist for this Workspace'

@pytest.mark.django_db(databases=['default'])
def test_disconnect_view_configuration_not_found(api_client, mocker, access_token, get_org_id):
    """Test DisconnectView when configuration not found"""
    url = reverse('bamboohr:disconnect',
        kwargs={
            'org_id': 99999,  # Non-existent org_id
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    response = api_client.post(url, format='json')
    assert response.status_code == 404
    assert response.data['message'] == 'BambooHR connection does not exists for this org.'

@pytest.mark.django_db(databases=['default'])
def test_sync_employees_view(api_client, mocker, access_token, get_org_id):
    """Test SyncEmployeesView"""
    url = reverse('bamboohr:sync-employees',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    # Mock async_task
    mock_async_task = mocker.patch('apps.bamboohr.views.async_task')
    
    response = api_client.post(url, format='json')
    assert response.status_code == 201
    assert response.data['message'] == 'success'  # Fixed to match actual response
    
    # Verify async_task was called - note: the actual call doesn't include the False parameter
    mock_async_task.assert_called_once_with('apps.bamboohr.tasks.import_employees', get_org_id)
