
import json
import pytest
from django.urls import reverse

from tests.helper import dict_compare_keys
from .fixtures import fixture


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
