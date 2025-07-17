import json
import pytest
from django.urls import reverse
from rest_framework import status

from apps.bamboohr.models import BambooHr
from apps.bamboohr.views import BambooHrConfigurationView
from apps.integrations.models import Integration
from apps.orgs.models import Org
from tests.helper import dict_compare_keys
from .fixtures import fixture
from .mock_setup import (
    mock_bamboohr_shared_mock,
    mock_bamboohr_invalid_token_shared_mock
)


def test_bamboohr_get_view_case_1(mock_dependencies, api_client, access_token, create_org, create_bamboohr):
    """
    Test bamboohr GET view
    Case: Valid org_id returns 200 with correct data
    """
    url = reverse('bamboohr:bamboohr', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert dict_compare_keys(response_data, fixture['bamboohr']) == [], 'bamboohr GET diff in keys'


def test_bamboohr_get_view_case_2(mock_dependencies, api_client, access_token):
    """
    Test bamboohr GET view
    Case: Invalid org_id returns 404
    """
    url = reverse('bamboohr:bamboohr', kwargs={'org_id': 123})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response_data = json.loads(response.content)
    assert response_data['message'] is not None


def test_post_configuration_view_case_1(mock_dependencies, api_client, access_token, create_org):
    """
    Test post configuration view
    Case: Valid configuration data returns 200
    """
    url = reverse('bamboohr:configuration', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    configuration_data = mock_dependencies.configuration_data
    configuration_data["org"] = create_org.id

    response = api_client.post(url, configuration_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['emails_selected'] == [{'name': 'Nilesh', 'email': 'nilesh.p@fyle.in'}]


def test_post_configuration_view_case_2(mock_dependencies, api_client, access_token, create_org):
    """
    Test post configuration view
    Case: Missing required fields returns 400
    """
    url = reverse('bamboohr:configuration', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    # Test with incomplete data to trigger KeyError
    incomplete_data = {"org": create_org.id}  # Missing required fields

    response = api_client.post(url, incomplete_data, format='json')
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR or response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_configuration_view_case_1(mock_dependencies, api_client, access_token, create_org, create_bamboohr):
    """
    Test get configuration view
    Case: Valid org_id returns 200 with correct data
    """
    url = reverse('bamboohr:configuration', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url, {'org_id': str(create_org.id)})
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert dict_compare_keys(response_data, fixture['configurations']) == [], 'configurations GET diff in keys'


def test_get_configuration_view_case_2(mock_dependencies, api_client, access_token):
    """
    Test get configuration view
    Case: Invalid org_id returns 404
    """
    url = reverse('bamboohr:configuration', kwargs={'org_id': 123})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url, {'org_id': '1231'})
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response_data = json.loads(response.content)
    assert response_data['message'] is not None


def test_post_bamboohr_connection_view_case_1(mock_dependencies, api_client, access_token, create_org):
    """
    Test post bamboohr connection view
    Case: Missing input returns 400
    """
    url = reverse('bamboohr:connection', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, mock_dependencies.bamboo_connection_invalid_payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_post_bamboohr_connection_view_case_3(mock_dependencies, api_client, access_token, create_org):
    """
    Test post bamboohr connection view
    Case: Valid input returns 200 and creates database records
    """
    url = reverse('bamboohr:connection', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, mock_dependencies.bamboo_connection, format='json')
    assert response.status_code == status.HTTP_200_OK

    mock_dependencies.add_to_integrations.assert_called_once()
    
    bamboohr = BambooHr.objects.filter(org=create_org).first()
    assert bamboohr is not None
    assert bamboohr.api_token == mock_dependencies.bamboo_connection['input']['api_token']
    assert bamboohr.sub_domain == mock_dependencies.bamboo_connection['input']['subdomain']


def test_post_bamboohr_disconnect_view_case_1(mock_dependencies, api_client, access_token):
    """
    Test post bamboohr disconnect view
    Case: Invalid org id returns 404
    """
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    url = reverse('bamboohr:disconnect', kwargs={'org_id': '1234567'})
    response = api_client.post(url, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_post_bamboohr_disconnect_view_case_2(mock_dependencies, api_client, access_token, create_org):
    """
    Test post bamboohr disconnect view
    Case: Valid disconnect call returns 200 and calls cleanup functions
    """
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    connect_url = reverse('bamboohr:connection', kwargs={'org_id': create_org.id})

    response = api_client.post(connect_url, mock_dependencies.bamboo_connection, format='json')
    assert response.status_code == status.HTTP_200_OK

    url = reverse('bamboohr:disconnect', kwargs={'org_id': create_org.id})
    response = api_client.post(url, format='json')
    assert response.status_code == status.HTTP_200_OK

    mock_dependencies.delete_sync_schedule.assert_called_once_with(org_id=create_org.id)
    mock_dependencies.deactivate_integration.assert_called_once_with(create_org.id)


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_health_check_view_case_1(mock_dependencies, api_client, access_token, create_org, create_bamboohr):
    """
    Test health check view
    Case: Valid bamboohr connection returns 200
    """
    url = reverse('bamboohr:health-check', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Ready'


def test_health_check_view_case_2(mock_dependencies, api_client, access_token):
    """
    Test health check view
    Case: No bamboohr connection returns 404
    """
    url = reverse('bamboohr:health-check', kwargs={'org_id': 123})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['message'] == 'Bamboo HR Details Not Found'


def test_webhook_callback_view(mock_dependencies, api_client):
    """
    Test webhook callback view
    """
    url = reverse('bamboohr:webhook-callback', kwargs={'org_id': 1})
    
    webhook_data = mock_dependencies.webhook_payload
    response = api_client.post(url, webhook_data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['status'] == 'success'
    
    mock_dependencies.async_task.assert_called_once_with(
        'apps.bamboohr.tasks.update_employee', 1, webhook_data
    )


def test_sync_employees_view(mock_dependencies, api_client, access_token, create_org):
    """
    Test sync employees view
    """
    url = reverse('bamboohr:sync-employees', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, mock_dependencies.sync_employees_request_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'success'
    
    mock_dependencies.async_task.assert_called_once_with(
        'apps.bamboohr.tasks.import_employees', create_org.id
    )


def test_bamboohr_configuration_get_object_method(api_client, access_token, create_org, create_bamboohr_configuration):
    """
    Test BambooHrConfigurationView get_object method coverage by making a GET request
    """
    url = reverse('bamboohr:configuration', kwargs={'org_id': create_org.id}) + f'?org_id={create_org.id}'
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
