
import json
import pytest
from django.urls import reverse

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