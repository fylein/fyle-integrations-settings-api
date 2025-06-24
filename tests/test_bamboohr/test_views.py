import json
import pytest
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient

from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.integrations.models import Integration
from apps.orgs.models import Org
from tests.helper import dict_compare_keys
from .fixtures import fixture
from .mock_setup import (
    mock_bamboohr_sdk_invalid_token_shared_mock,
    mock_bamboohr_connection_shared_mock,
    mock_bamboohr_sdk_error_response_shared_mock,
    mock_bamboohr_async_task_shared_mock
)
from bamboosdk.exceptions import InvalidTokenError


def test_bamboohr_get_view_case_1(api_client, mocker, access_token, get_org_id, get_bamboohr_id, db):
    """
    Test BambooHR Get View
    Case: successful retrieval
    """
    url = reverse('bamboohr:bamboohr',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_post_configuration_view_case_1(api_client, mocker, access_token, get_org_id, db):
    """
    Test Post Configuration View
    Case: successful configuration creation
    """
    url = reverse('bamboohr:configuration',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Create org first to avoid DoesNotExist error
    org, created = Org.objects.get_or_create(
        id=get_org_id, 
        defaults={'name': 'Test Org', 'fyle_org_id': 'test_org_id'}
    )

    # Mock the signal handler to avoid the org access issue
    mocker.patch('apps.bamboohr.signals.run_post_save_configurations')
    
    # Also mock the schedule_sync_employees function
    mocker.patch('apps.bamboohr.signals.schedule_sync_employees')
    
    # Mock the signal at the module level to prevent it from being called
    mocker.patch('django.db.models.signals.post_save.send')

    # Update the fixture data to use the correct org_id
    test_data = fixture['bamboo_configuration'].copy()
    test_data['org'] = get_org_id

    response = api_client.post(url, test_data, format='json')
    assert response.status_code == status.HTTP_200_OK


def test_get_configuration_view_case_1(api_client, mocker, access_token, get_org_id, get_bamboohr_id, db):
    """
    Test Get Configuration View
    Case: successful configuration retrieval
    """
    url = reverse('bamboohr:configuration',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Create org and configuration first
    org, created = Org.objects.get_or_create(
        id=get_org_id, 
        defaults={'name': 'Test Org', 'fyle_org_id': 'test_org_id'}
    )
    BambooHrConfiguration.objects.get_or_create(
        org=org,
        defaults={
            'additional_email_options': [{"name": "Test User", "email": "test@example.com"}],
            'emails_selected': ["test@example.com"]
        }
    )

    response = api_client.get(url, {'org_id': get_org_id})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_connection_shared_mock(mocker))
def test_post_bamboohr_connection_view_with_shared_mocks_case_1(api_client, access_token, get_org_id, mock_dependencies, db):
    """
    Test Post BambooHR Connection View with shared mocks
    Case: successful connection with shared mocks
    """
    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == status.HTTP_200_OK

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

    # Verify mock was called
    mock_dependencies.mock_bamboohr_sdk.time_off.get.assert_called_once()


def test_post_bamboohr_connection_view_case_1(api_client, mocker, access_token, get_org_id, db):
    """
    Test Post BambooHR Connection View
    Case: successful connection
    """
    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Missing input should return 400
    response = api_client.post(url, fixture['bamboo_connection_invalid_payload'], format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Invalid token should return 400
    mock_bamboohr_sdk_error_response_shared_mock(mocker, {})
    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Valid input should return 200
    mock_bamboohr_connection_shared_mock(mocker)
    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == status.HTTP_200_OK

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


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_sdk_invalid_token_shared_mock(mocker))
def test_bamboohr_connection_invalid_token_with_shared_mocks_case_1(api_client, access_token, get_org_id, mock_dependencies, db):
    """
    Test BambooHR connection with invalid token using shared mocks
    Case: invalid token handling with shared mocks
    """
    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Invalid token should return 400
    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Verify mock was called
    mock_dependencies.mock_bamboohr_sdk.time_off.get.assert_called_once()


def test_post_bamboohr_disconnect_view_case_1(api_client, mocker, access_token, get_org_id, db):
    """
    Test Post BambooHR Disconnect View
    Case: successful disconnection
    """
    # Create a BambooHr connection for the org
    BambooHr.objects.create(org_id=get_org_id, is_credentials_expired=False)
    # Create an Integration for the org
    org = Org.objects.get(id=get_org_id)
    Integration.objects.create(
        org_id=org.fyle_org_id,
        type='HRMS',
        is_active=True,
        org_name=org.name,
        tpa_id=settings.FYLE_CLIENT_ID,
        tpa_name='Fyle BambooHR Integration'
    )

    url = reverse('bamboohr:disconnect',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Use shared mock for BambooHrSDK
    mock_bamboohr_connection_shared_mock(mocker)

    response = api_client.post(url, format='json')
    assert response.status_code == status.HTTP_200_OK

    # Verify integration was deactivated
    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    integration_object = Integration.objects.get(org_id=org.fyle_org_id, type='HRMS')
    assert integration_object
    assert integration_object.is_active is False
    assert integration_object.disconnected_at is not None


def test_health_check_bamboohr_not_found_case_1(api_client, mocker, access_token, get_org_id, db):
    """
    Test health check when BambooHR not found
    Case: bamboohr configuration not found
    """

    url = reverse('bamboohr:health-check',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("mock_response,expected_message", [
    (InvalidTokenError('Invalid token'), 'Invalid token'),
    ({'timeOffTypes': []}, 'Invalid token'),
])
def test_health_check_error_scenarios_case_1(api_client, mocker, access_token, get_org_id, get_bamboohr_id, mock_response, expected_message, db):
    """
    Test health check error scenarios
    Case: various error conditions
    """

    url = reverse('bamboohr:health-check',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Use shared mock for error responses
    mock_bamboohr_sdk_error_response_shared_mock(mocker, mock_response)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_webhook_callback_api_view_case_1(api_client, mocker, access_token, get_org_id, db):
    """
    Test webhook callback API view
    Case: successful webhook processing
    """
    url = reverse('bamboohr:webhook-callback',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    webhook_data = {
        'type': 'employee_updated',
        'employee_id': 123
    }

    # Use shared mock for async task
    mock_deps = mock_bamboohr_async_task_shared_mock(mocker)

    response = api_client.post(url, webhook_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    mock_deps['mock_async_task'].assert_called_once_with('apps.bamboohr.tasks.update_employee', get_org_id, webhook_data)


def test_bamboohr_connection_missing_input_case_1(api_client, mocker, access_token, get_org_id, db):
    """
    Test BambooHR connection with missing input
    Case: missing required input fields
    """

    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Missing input should return 400
    response = api_client.post(url, {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("mock_response,expected_message", [
    (InvalidTokenError('Invalid token'), 'Invalid token'),
    ({'timeOffTypes': []}, 'Invalid token'),
])
def test_bamboohr_connection_error_scenarios_case_1(api_client, mocker, access_token, get_org_id, mock_response, expected_message, db):
    """
    Test BambooHR connection error scenarios
    Case: various connection error conditions
    """

    url = reverse('bamboohr:connection',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Use shared mock for error responses
    mock_bamboohr_sdk_error_response_shared_mock(mocker, mock_response)

    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("org_id,expected_message", [
    (99999, 'BambooHr Configuration does not exist for this Workspace'),
    (99999, 'BambooHR connection does not exists for this org.'),
])
def test_not_found_scenarios_case_1(api_client, mocker, access_token, get_org_id, org_id, expected_message, db):
    """
    Test not found scenarios
    Case: various not found conditions
    """

    url = reverse('bamboohr:configuration',
        kwargs={
            'org_id': org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_sync_employees_view_case_1(api_client, mocker, access_token, get_org_id, db):
    """
    Test sync employees view
    Case: successful employee sync
    """
    url = reverse('bamboohr:sync-employees',
        kwargs={
            'org_id': get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Use shared mock for async task
    mock_deps = mock_bamboohr_async_task_shared_mock(mocker)

    response = api_client.post(url, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # The actual call only passes 2 parameters, not 3
    mock_deps['mock_async_task'].assert_called_once_with('apps.bamboohr.tasks.import_employees', get_org_id)
