import json

from apps.integrations.models import Integration
import pytest
from django.urls import reverse
from .fixture import post_integration_accounting, post_integration_accounting_2, post_integration_hrms, patch_integration_no_tpa_name, patch_integration, patch_integration_invalid_tpa_name, patch_integration_partial


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_post_accounting(api_client, mocker, access_token):
    """
    Test POST of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
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
    assert response['is_beta'] == True
    assert response['disconnected_at'] == None

    api_client.post(url, post_integration_accounting_2)

    api_client.post(url, post_integration_hrms)

    response = api_client.get(url)
    response = json.loads(response.content)

    assert response[0]['type'] == 'ACCOUNTING'
    assert response[1]['type'] == 'HRMS'
    assert response[0]['updated_at'] < response[1]['updated_at']


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_post(api_client, mocker, access_token):
    """
    Test POST of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
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
    assert response['is_beta'] == True
    assert response['disconnected_at'] == None

    accounting_integration_id = response['id']

    response = api_client.post(url, post_integration_hrms)
    assert response.status_code == 201

    response = json.loads(response.content)

    assert response['org_id'] == dummy_org_id
    assert response['tpa_id'] == post_integration_hrms['tpa_id']
    assert response['tpa_name'] == post_integration_hrms['tpa_name']
    assert response['type'] == post_integration_hrms['type']
    assert response['is_active'] == post_integration_hrms['is_active']
    assert response['is_beta'] == True
    assert response['disconnected_at'] == None


    # A second POST with the same org_id and type should update the record

    response = api_client.post(url, post_integration_accounting_2)
    assert response.status_code == 201

    response = json.loads(response.content)

    # Check if a record was updated, and no new record was inserted
    assert response['id'] == accounting_integration_id
    assert Integration.objects.filter(org_id=dummy_org_id).count() == 2

    # Check if the updates went through
    assert response['org_id'] == dummy_org_id
    assert response['tpa_id'] == post_integration_accounting_2['tpa_id']
    assert response['tpa_name'] == post_integration_accounting_2['tpa_name']
    assert response['type'] == post_integration_accounting_2['type']
    assert response['is_active'] == post_integration_accounting_2['is_active']
    assert response['is_beta'] == True
    assert response['disconnected_at'] == None


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_get(api_client, mocker, access_token, create_integrations):
    """
    Test GET of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
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
    assert response.status_code == 403

    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == 403

    response = api_client.patch(url, post_integration_accounting)
    assert response.status_code == 403


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_mark_inactive_post(api_client, mocker, access_token, create_integrations):
    """
    Test POST of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
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

    # Marking inactive integration back to active
    payload = dict(post_integration_accounting)

    response = api_client.post(url, payload)
    assert response.status_code == 201

    response = json.loads(response.content)
    assert response['is_active'] == True


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_patch(api_client, mocker, access_token):
    """
    Test the PATCH API of Integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )

    Integration.objects.create(
        org_id=dummy_org_id,
        tpa_name=patch_integration['tpa_name'],
        tpa_id='tpa129sjcjkjx',
        type='ACCOUNTING',
        is_active=True
    )

    url = reverse('integrations:integrations')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))


    response = api_client.patch(url,  json.dumps(patch_integration_no_tpa_name), content_type="application/json")
    assert response.status_code == 400, 'PATCH without a tpa_name should return 400'

    response = api_client.patch(url,  json.dumps(patch_integration_invalid_tpa_name), content_type="application/json")
    assert response.status_code == 400, 'PATCH with an invalid tpa_name should return 400'

    # Update two fields
    response = api_client.patch(url,  json.dumps(patch_integration), content_type="application/json")
    assert response.status_code == 200, 'Valid PATCH request should be successful'

    response = json.loads(response.content)
    assert response['tpa_name'] == patch_integration['tpa_name']
    assert response['errors_count'] == patch_integration['errors_count']
    assert response['is_token_expired'] == patch_integration['is_token_expired']

    # Update one field, leaving the other as it is
    response = api_client.patch(url, json.dumps(patch_integration_partial), content_type="application/json")
    assert response.status_code == 200, 'Valid PATCH request should be successful'

    response = json.loads(response.content)
    assert response['tpa_name'] == patch_integration_partial['tpa_name']
    assert response['is_token_expired'] == patch_integration_partial['is_token_expired']
    assert response['errors_count'] == patch_integration['errors_count']