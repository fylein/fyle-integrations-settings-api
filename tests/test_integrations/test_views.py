import json

import pytest
from django.urls import reverse
from .fixture import mock_post_new_integration_response, post_integration_accounting, post_integration_hrms


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_post_accounting(api_client, mocker, access_token):
    """
    Test POST of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_from_access_token',
        return_value=dummy_org_id
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )

    url = reverse('integrations:integrations')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == 201

    response = json.loads(response.content)

    assert response['org_id'] == dummy_org_id
    assert response['tpa_id'] == post_integration_accounting['tpa_id']
    assert response['tpa_name'] == post_integration_accounting['tpa_name']
    assert response['type'] == post_integration_accounting['type']
    assert response['is_active'] == post_integration_accounting['is_active']
    assert response['is_beta'] == False
    assert response['disconnected_at'] == None


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_post(api_client, mocker, access_token):
    """
    Test POST of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_from_access_token',
        return_value=dummy_org_id
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )

    url = reverse('integrations:integrations')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == 201

    response = json.loads(response.content)

    assert response['org_id'] == dummy_org_id
    assert response['tpa_id'] == post_integration_accounting['tpa_id']
    assert response['tpa_name'] == post_integration_accounting['tpa_name']
    assert response['type'] == post_integration_accounting['type']
    assert response['is_active'] == post_integration_accounting['is_active']
    assert response['is_beta'] == False
    assert response['disconnected_at'] == None

    response = api_client.post(url, post_integration_hrms)
    assert response.status_code == 201

    response = json.loads(response.content)

    assert response['org_id'] == dummy_org_id
    assert response['tpa_id'] == post_integration_hrms['tpa_id']
    assert response['tpa_name'] == post_integration_hrms['tpa_name']
    assert response['type'] == post_integration_hrms['type']
    assert response['is_active'] == post_integration_hrms['is_active']
    assert response['is_beta'] == False
    assert response['disconnected_at'] == None


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_get(api_client, mocker, access_token, create_integrations):
    """
    Test GET of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_from_access_token',
        return_value=dummy_org_id
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )

    url = reverse('integrations:integrations')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert len(response) == 2

    response = api_client.get(url, {'type': 'ACCOUNTING'})
    assert response.status_code == 200

    response = json.loads(response.content)
    assert len(response) == 1

    assert response[0]['org_id'] == dummy_org_id
    assert response[0]['tpa_id'] == post_integration_accounting['tpa_id']
    assert response[0]['tpa_name'] == post_integration_accounting['tpa_name']
    assert response[0]['type'] == post_integration_accounting['type']
    assert response[0]['is_active'] == post_integration_accounting['is_active']
    assert response[0]['is_beta'] == True
    assert response[0]['disconnected_at'] == None

    response = api_client.get(url, {'type': 'HRMS'})
    assert response.status_code == 200

    response = json.loads(response.content)
    assert len(response) == 1

    assert response[0]['org_id'] == dummy_org_id
    assert response[0]['tpa_id'] == post_integration_hrms['tpa_id']
    assert response[0]['tpa_name'] == post_integration_hrms['tpa_name']
    assert response[0]['type'] == post_integration_hrms['type']
    assert response[0]['is_active'] == post_integration_hrms['is_active']
    assert response[0]['is_beta'] == True
    assert response[0]['disconnected_at'] == None


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_invalid_access_token(api_client):
    url = reverse('integrations:integrations')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer ey.ey.ey')

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert len(response) == 0

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == 403


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_mark_inactive_post(api_client, mocker, access_token, create_integrations):
    """
    Test POST of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_from_access_token',
        return_value=dummy_org_id
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )

    url = reverse('integrations:integrations')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    payload = dict(post_integration_accounting)
    payload['is_active'] = False

    response = api_client.post(url, payload)
    assert response.status_code == 201

    response = json.loads(response.content)

    assert response['org_id'] == dummy_org_id
    assert response['tpa_id'] == post_integration_accounting['tpa_id']
    assert response['tpa_name'] == post_integration_accounting['tpa_name']
    assert response['type'] == post_integration_accounting['type']
    assert response['is_active'] == False
    assert response['is_beta'] == True
    assert response['disconnected_at'] != None
