
import json
import pytest
from unittest import mock
from django.urls import reverse

from workato.exceptions import *
from tests.helper import dict_compare_keys
from .fixtures import fixture

@pytest.mark.django_db(databases=['default'])
def test_bamboohr_get_view(api_client, mocker, access_token):
    """
    Test Get of Orgs
    """
    url = reverse('bamboohr',
        kwargs={
                'org_id': 1,
            }
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['bamboohr']) == [], 'orgs GET diff in keys'

    url = reverse('bamboohr',
        kwargs={
                'org_id': 123,
            }
    )
    response = api_client.get(url)
    assert response.status_code == 400

    response = json.loads(response.content)
    assert response['message'] != None


@pytest.mark.django_db(databases=['default'])
def test_post_folder_view(api_client, mocker, access_token):
    """
    Test Post Of Folder
    """

    url = reverse('folder',
        kwargs={
                'org_id': 3,
            }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    with mock.patch('workato.workato.Folders.post', side_effect=BadRequestError({'message': 'something wrong happened'})):
        response = api_client.post(url)
        assert response.data['message'] == 'something wrong happened'
        assert response.status_code == 400
    
    mocker.patch(
        'workato.workato.Folders.post',
        return_value={'id': 'dummy'}
    )

    response = api_client.post(url)
    
    assert response.status_code == 200
    assert dict_compare_keys(response, fixture['bamboohr']) == [], 'Bamboohr diff in keys'

    mocker.patch(
        'workato.workato.Folders.post',
        return_value={}
    )
    
    response = api_client.post(url)
    
    assert response.status_code == 400
    assert response.data['message'] == 'Error in Creating Folder'


@pytest.mark.django_db(databases=['default'])
def test_post_package(api_client, mocker, access_token):
    """
    Test Posting Package in Workato
    """
    
    url = reverse('package',
        kwargs={
            'org_id': 1
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    with mock.patch('workato.workato.Packages.post', side_effect=BadRequestError({'message': 'something wrong happened'})):
        response = api_client.post(url)
        assert response.data['message'] == 'something wrong happened'
        assert response.status_code == 400

    mocker.patch(
        'workato.workato.Packages.post',
        return_value={}
    )
    
    response = api_client.post(url)
    assert response.status_code == 400
    assert response.data['message'] == 'Error in Uploading Package'

    mocker.patch(
        'workato.workato.Packages.post',
        return_value={'id': 'dummy'}
    )

    mocker.patch(
        'workato.workato.Packages.get',
        return_value={'status': 'completed'}
    )

    response = api_client.post(url)
    assert response.status_code == 200
    assert response.data['message'] == 'package uploaded successfully'


@pytest.mark.django_db(databases=['default'])
def test_bamboohr_connection(api_client, mocker, access_token):
    """
    Test Creating Bamboohr Connection In Workato
    """
    
    url = reverse('bamboo-connection',
        kwargs={
            'org_id':1,
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
    
    data = {
        'input': {
            'api_token': 'dummy',
            'subdomain': 'dummy'
        }
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == 400
    assert response.data['message'] == 'Error Creating Bamboo HR Connection in Recipe'

    mocker.patch(
        'workato.workato.Connections.get',
        return_value=fixture['connections']
    )

    mocker.patch(
        'workato.workato.Connections.put',
        return_value={'message': 'success', 'authorization_status': 'success'}
    )


    response = api_client.post(url, data, format='json')
    
    assert response.status_code == 200
    assert dict_compare_keys(response, fixture['bamboohr']) == [], 'Bamboohr diff in keys'


@pytest.mark.django_db(databases=['default'])
def test_post_configuration_view(api_client, mocker, access_token):
    """
    Test Post Configuration View
    """

    url = reverse('configuration',
        kwargs={
            'org_id': 2,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    mocker.patch(
        'workato.workato.Recipes.get',
        return_value=fixture['recipes']
    )
    mocker.patch(
        'workato.workato.Recipes.post',
        return_value={'message': 'success'}
    )
    response = api_client.post(url,
        {
            "org": 2,
            "additional_email_options": {},
            "emails_selected": [
                {
                    "name": "Nilesh",
                    "email": "nilesh.p@fyle.in"
                },
            ]
        }, format='json'
    )

    assert response.status_code == 201
    assert response.data['recipe_id'] == '3545113'
    assert response.data['emails_selected'] ==  [{'name': 'Nilesh', 'email': 'nilesh.p@fyle.in'}]


@pytest.mark.django_db(databases=['default'])
def test_get_configuration_view(api_client, mocker, access_token):
    """
    Test Get Configuration View
    """

    url = reverse('configuration',
        kwargs={
            'org_id':1,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url, {'org_id': '1'})
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['configurations']) == [], 'orgs GET diff in keys'

    response = api_client.get(url, {'org_id': '1231'})
    assert response.status_code == 400

    response = json.loads(response.content)
    assert response['message'] != None


@pytest.mark.django_db(databases=['default'])
def test_sync_employees_view(api_client, mocker, access_token):
    """
    Test Sync Of Employees In Workato
    """

    url = reverse('sync-employees',
        kwargs={
            'org_id':1,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    with mock.patch('workato.workato.Recipes.get', side_effect=NotFoundItemError({'message': 'Item Not Found'})):
        response = api_client.post(url)
        assert response.data['message'] == 'Item Not Found'
        assert response.status_code == 404

    mocker.patch(
        'workato.workato.Recipes.get',
        return_value=fixture['recipes']
    )
    mocker.patch(
        'workato.workato.Recipes.post',
        return_value={'message': 'success'}
    )

    response = api_client.post(url)
    assert response.status_code == 200


@pytest.mark.django_db(databases=['default'])
def test_disconnect_view(api_client, mocker, access_token):
    """
    Test Start and Stop Of Recipes In Workato
    """

    url = reverse('disconnect',
        kwargs={
            'org_id':1,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    data = {
        'payload': 'start'
    }

    mocker.patch(
        'workato.workato.Connections.get',
        return_value=fixture['connections']
    )

    mocker.patch(
        'workato.workato.Connections.post',
        return_value={'message': 'success'}
    )


    with mock.patch('workato.workato.Recipes.post', side_effect=NotFoundItemError({'message': 'Not found'})):
        response = api_client.post(url, data, json=True)
        assert response.data['message'] == 'Not found'
        assert response.status_code == 404

    mocker.patch(
        'workato.workato.Recipes.post',
        return_value={'message': 'success'}
    )

    response = api_client.post(url, data, json=True)
    assert response.status_code == 200
