
import json
import pytest
from unittest import mock
from django.urls import reverse

from workato.exceptions import *
from tests.helper import dict_compare_keys
from .fixtures import fixture

@pytest.mark.django_db(databases=['default'])
def test_travelperk_get_view(api_client, access_token):
    """
    Test Get of Travelperk
    """
    url = reverse('travelperk',
        kwargs={
                'org_id': 1,
            }
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['travelperk']) == [], 'orgs GET diff in keys'

    url = reverse('travelperk',
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

    url = reverse('travelperk-folder',
        kwargs={
                'org_id': 21,
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
    assert dict_compare_keys(response, fixture['travelperk']) == [], 'Bamboohr diff in keys'

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
    
    url = reverse('travelperk-package',
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
def test_get_configuration_view(api_client, mocker, access_token):
    """
    Test Get Configuration View
    """

    url = reverse('travelperk-configuration',
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
def test_fyle_connection(api_client, mocker, access_token):
    """
    Test Creating Fyle Connection In Workato
    """
    url = reverse('fyle-travelperk-connection',
        kwargs={
            'org_id': 1,
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
    assert response.data['message'] == 'connection failed'

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
def test_aws_connection(api_client, mocker, access_token):
    """
    Test Creating AWS S3 Connection In Workato
    """

    url = reverse('s3-connection',
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

    response = api_client.post(url)
    assert response.status_code == 400
    assert response.data['message'] == 'Error Creating AWS Connection in Recipe'

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
def test_post_configuration_view(api_client, mocker, access_token):
    """
    Test Post Configuration View
    """

    url = reverse('travelperk-configuration',
        kwargs={
            'org_id': 26,
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
          "org": 26,
        }, format='json'
    )

    assert response.status_code == 201
    assert response.data['recipe_id'] == '3545113'

@pytest.mark.django_db(databases=['default'])
def test_recipe_status_view(api_client, access_token):
    
    url = reverse(
        kwargs={
            'org_id': 1,
            'status': True
        }
    )
    
    response = api_client.post(url, {'org_id': 1, 'status': True}, format='json')
    
    assert response.status_code == 200
    assert response.data['is_recipe_enabled'] == True
