
import json
import pytest
from unittest import mock
from django.urls import reverse

from workato.exceptions import *
from tests.helper import dict_compare_keys
from .fixtures import fixture


@pytest.mark.django_db(databases=['default'])
def test_gusto_get_view(api_client, mocker, access_token, get_org_id, get_gusto_id):
    """
    Test Get of Gusto
    """
    url = reverse('gusto',
        kwargs={
                'org_id': get_org_id,
            }
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['gusto']) == [], 'orgs GET diff in keys'

    url = reverse('gusto',
        kwargs={
                'org_id': 123,
            }
    )
    response = api_client.get(url)
    assert response.status_code == 404

    response = json.loads(response.content)
    assert response['message'] != None


@pytest.mark.django_db(databases=['default'])
def test_post_folder_view(api_client, mocker, access_token, get_org_id, get_gusto_id):
    """
    Test Post Of Folder
    """

    url = reverse('gusto_folder',
        kwargs={
                'org_id': get_org_id,
            }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    mocker.patch(
        'workato.workato.Properties.post',
        return_value = None
    )

    with mock.patch('workato.workato.Folders.post', side_effect=BadRequestError({'message': 'something wrong happened'})):
        response = api_client.post(url)
        assert response.data['message'] == {'message': 'something wrong happened'}
        assert response.status_code == 400
    
    mocker.patch(
        'workato.workato.Folders.post',
        return_value={'id': 'dummy'}
    )

    response = api_client.post(url)
    
    assert response.status_code == 200
    assert dict_compare_keys(response, fixture['gusto']) == [], 'gusto diff in keys'


@pytest.mark.django_db(databases=['default'])
def test_post_package(api_client, mocker, access_token, get_org_id, get_gusto_id):
    """
    Test Posting Package in Workato
    """
    
    url = reverse('gusto_package',
        kwargs={
            'org_id': get_org_id
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    with mock.patch('workato.workato.Packages.post', side_effect=BadRequestError({'message': 'something wrong happened'})):
        response = api_client.post(url)
        assert response.data['message'] == {'message': 'something wrong happened'}
        assert response.status_code == 400

    mocker.patch(
        'workato.workato.Packages.post',
        return_value={}
    )
    
    response = api_client.post(url)
    assert response.status_code == 500
    assert response.data['message'] == 'Something went wrong'

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
def test_post_configuration_view(api_client, mocker, access_token, get_org_id, get_gusto_id):
    """
    Test Post Configuration View
    """

    url = reverse('gusto_configuration',
        kwargs={
            'org_id': get_org_id,
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
    response = api_client.post(url, {
            "org": get_org_id,
            "additional_email_options": {},
            "emails_selected": [{
            "name": "Ashwin",
            "email": "ashwin.t@fyle.in"
        }
        ]}, format='json'
    )

    assert response.status_code == 201
    assert response.data['recipe_id'] == '6368872'
    assert response.data['emails_selected'] == [
        {
            "name": "Ashwin",
            "email": "ashwin.t@fyle.in"
        }
    ]

@pytest.mark.django_db(databases=['default'])
def test_get_configuration_view(api_client, mocker, access_token, get_org_id, get_gusto_id):
    """
    Test Get Configuration View
    """

    url = reverse('gusto_configuration',
        kwargs={
            'org_id':get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url, {'org_id': 1})
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['configurations']) == [], 'orgs GET diff in keys'

    url = reverse('gusto_configuration',
        kwargs={
            'org_id':1231,
        }
    )

    response = api_client.get(url, {'org_id': '1231'})
    assert response.status_code == 400

    response = json.loads(response.content)
    assert response['message'] != None


@pytest.mark.django_db(databases=['default'])
def test_sync_employees_view(api_client, mocker, access_token, get_org_id, get_gusto_id):
    """
    Test Sync Of Employees In Workato
    """

    url = reverse('gusto_sync_employees',
        kwargs={
            'org_id':get_org_id,
        }
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    with mock.patch('workato.workato.Recipes.get', side_effect=NotFoundItemError({'message': 'Item Not Found'})):
        response = api_client.post(url)
        assert response.data['message'] == 'Item Not Found'
        assert response.status_code == 404

    with mock.patch('workato.workato.Recipes.get', side_effect=InternalServerError({'message': 'Internal server error'})):
        response = api_client.post(url)
        assert response.data['message'] == 'Error in Syncing Employees in Gusto'
        assert response.status_code == 500

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
    assert response.data['name'] == 'Gusto Sync Recipe'

@pytest.mark.django_db(databases=['default'])
def test_gusto_connection(api_client, mocker, access_token, get_org_id, get_gusto_id):
    """
    Test Creating Gusto Connection In Workato
    """
    
    url = reverse('gusto_fyle_connection',
        kwargs={
            'org_id':get_org_id,
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
    
    response = api_client.post(url, format='json')
    assert response.status_code == 400
    assert response.data['message'] == 'Error Creating Gusto Connection in Recipe'

    mocker.patch(
        'workato.workato.Connections.get',
        return_value=fixture['connections']
    )

    mocker.patch(
        'workato.workato.Connections.put',
        return_value={'message': 'success', 'authorization_status': 'success'}
    )


    response = api_client.post(url, format='json')
    
    assert response.status_code == 200
    assert dict_compare_keys(response, fixture['gusto']) == [], 'gusto diff in keys'

@pytest.mark.django_db(databases=['default'])
def test_recipe_status_view(api_client, mocker, access_token, get_org_id, get_gusto_id):
    """
    Test Get of Gusto
    """
    url = reverse('gusto_recipe_status',
        kwargs={
                'org_id': get_org_id,
            }
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    mocker.patch(
        'workato.workato.Recipes.post',
        return_value={'message': 'success'}
    )

    response = api_client.put(url, data = {
        'recipe_status' : False
    })
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['configurations']) == [], 'orgs GET diff in keys'
