import json
import pytest
from django.urls import reverse
from rest_framework import status

from apps.bamboohr.models import BambooHr
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


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_invalid_token_shared_mock(mocker))
def test_post_bamboohr_connection_view_case_2(mock_dependencies, api_client, access_token, create_org):
    """
    Test post bamboohr connection view
    Case: Invalid token returns 400
    """
    url = reverse('bamboohr:connection', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, mock_dependencies.bamboo_connection, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_post_bamboohr_connection_view_case_3(mock_dependencies, api_client, access_token, create_org):
    """
    Test post bamboohr connection view
    Case: Valid input returns 200 and creates integration
    """
    url = reverse('bamboohr:connection', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, mock_dependencies.bamboo_connection, format='json')
    assert response.status_code == status.HTTP_200_OK

    integration_object = Integration.objects.get(org_id=create_org.fyle_org_id, type='HRMS')
    assert integration_object is not None
    assert integration_object.tpa_name == mock_dependencies.integrations_response['tpa_name']
    assert integration_object.tpa_id == mock_dependencies.integrations_response['tpa_id']
    assert integration_object.type == mock_dependencies.integrations_response['type']
    assert integration_object.org_id == create_org.fyle_org_id
    assert integration_object.org_name == create_org.name
    assert integration_object.is_active is True
    assert integration_object.is_beta is True


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
    Case: Valid disconnect call returns 200 and updates integration
    """
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    connect_url = reverse('bamboohr:connection', kwargs={'org_id': create_org.id})

    response = api_client.post(connect_url, mock_dependencies.bamboo_connection, format='json')
    assert response.status_code == status.HTTP_200_OK

    url = reverse('bamboohr:disconnect', kwargs={'org_id': create_org.id})
    response = api_client.post(url, format='json')
    assert response.status_code == status.HTTP_200_OK

    integration_object = Integration.objects.get(org_id=create_org.fyle_org_id, type='HRMS')
    assert integration_object.is_active is False
    assert integration_object.disconnected_at is not None
