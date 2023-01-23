
import json
import pytest
from unittest import mock

from django.urls import reverse

from tests.helper import dict_compare_keys
from .fixtures import fixture

from workato.exceptions import *


@pytest.mark.django_db(databases=['default'])
def test_ready_view(api_client, mocker, access_token):
    """"
    Test Get of Ready state
    """
    url = reverse('ready')
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db(databases=['default'])
def test_orgs_get_view(api_client, mocker, access_token):
    """
    Test Get of Orgs
    """
    url = reverse('orgs')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url, {'org_id': 'orHVw3ikkCxJ'})
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['orgs']) == [], 'orgs GET diff in keys'

    response = api_client.get(url, {'org_id': 'wrong_org_id'})
    assert response.status_code == 400

    response = json.loads(response.content)
    assert response['message'] != None
    
@pytest.mark.django_db(databases=['default'])
def test_orgs_put_view(api_client, mocker, access_token):
    """
    Test Put of Partner Orgs
    """
    url = reverse('orgs')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.put(url)
    assert response.status_code == 200

@pytest.mark.django_db(databases=['default'])
def test_new_org_put_view(api_client, mocker, access_token):
    """
    Test Put of New Partner Org
    """
    mocker.patch(
        'apps.orgs.serializers.get_fyle_admin',
        return_value=fixture['my_profile_admin']
    )

    url = reverse('orgs')

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.put(url)
    assert response.status_code == 200

@pytest.mark.django_db(databases=['default'])
def test_create_managed_user_in_workato(api_client, mocker, access_token):
    """
    Test Create of Workato Workspace
    """
    url = reverse('workato-workspace',
        kwargs={
            'org_id': 16,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    
    with mock.patch('apps.orgs.views.create_managed_user_and_set_properties', side_effect=BadRequestError({'message': 'something wrong happened'})):
        response = api_client.put(url)
        assert response.data['message'] == 'something wrong happened'
        assert response.status_code == 400

    with mock.patch('apps.orgs.views.create_managed_user_and_set_properties', side_effect=InternalServerError({'message': 'internal server error'})):
        response = api_client.put(url)
        assert response.data['message'] == 'internal server error'
        assert response.status_code == 500
    
    mocker.patch(
        'workato.workato.ManagedUser.post',
        return_value={}
    )

    response = api_client.put(url)

    assert response.status_code == 400
    assert response.data['message'] == 'Error in Creating Workato Workspace'
    
    mocker.patch(
        'workato.workato.ManagedUser.post',
        return_value=fixture['managed_user']
    )

    mocker.patch(
        'workato.workato.Properties.post',
        return_value={'message': 'success'}
    )


    response = api_client.put(url)
    
    assert response.status_code == 200
    assert response.data == fixture['managed_user']

@pytest.mark.django_db(databases=['default'])
def test_fyle_connection(api_client, mocker, access_token):
    """
    Test Creating Fyle Connection In Workato
    """
    url = reverse('fyle-connection',
        kwargs={
            'org_id': 17,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    with mock.patch('workato.workato.Connections.get', side_effect=BadRequestError({'message': 'something wrong happened'})):
        response = api_client.post(url)
        assert response.data['message'] == 'something wrong happened'
        assert response.status_code == 400

    mocker.patch(
        'workato.workato.Connections.get',
        return_value={'result': [{}]}
    )
    
    response = api_client.post(url)
    assert response.status_code == 400
    assert response.data['message'] == 'Error Creating Fyle Connection in Recipe'

    mocker.patch(
        'workato.workato.Connections.get',
        return_value=fixture['connections']
    )

    mocker.patch(
        'workato.workato.Connections.put',
        return_value={'message': 'failed', 'authorization_status': 'failed'}
    )

    response = api_client.post(url)
    assert response.status_code == 400
    assert response.data == {'message': 'connection failed'}

    mocker.patch(
        'workato.workato.Connections.put',
        return_value={'message': 'success', 'authorization_status': 'success'}
    )

    response = api_client.post(url)
    assert response.status_code == 200
    assert response.data == {'message': 'success', 'authorization_status': 'success'}

@pytest.mark.django_db(databases=['default'])
def test_sendgrid_connection(api_client, mocker, access_token):
    """
    Test Creating Sendgrid Connection In Workato
    """

    url = reverse('sendgrid',
        kwargs={
            'org_id':18,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    with mock.patch('workato.workato.Connections.get', side_effect=BadRequestError({'message': 'something wrong happened'})):
        response = api_client.post(url)
        assert response.data['message'] == 'something wrong happened'
        assert response.status_code == 400

    mocker.patch(
        'workato.workato.Connections.get',
        return_value={'result': [{}]}
    )

    response = api_client.post(url)
    assert response.status_code == 400
    assert response.data['message'] == 'Error Creating Sendgrid Connection in Recipe'

    mocker.patch(
        'workato.workato.Connections.get',
        return_value=fixture['connections']
    )

    mocker.patch(
        'workato.workato.Connections.put',
        return_value={'message': 'failed', 'authorization_status': 'failed'}
    )

    response = api_client.post(url)
    assert response.status_code == 400
    assert response.data == {'message': 'connection failed'}

    mocker.patch(
        'workato.workato.Connections.put',
        return_value={'message': 'success', 'authorization_status': 'success'}
    )

    response = api_client.post(url)
    
    assert response.status_code == 200
    assert response.data == {'message': 'success', 'authorization_status': 'success'}

@pytest.mark.django_db(databases=['default'])
def test_admin_view(api_client, mocker, access_token):
    """
    Test Admin View
    """
    url = reverse('admin-view',
        kwargs={
            'org_id':1,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    mocker.patch(
        'fyle.platform.apis.v1beta.admin.employees.list_all',
        return_value=[fixture['users']]
    )

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data == [{ "email": "abc@ac.com", "name": "abc"}]
