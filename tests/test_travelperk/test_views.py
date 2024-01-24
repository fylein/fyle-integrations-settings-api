
import json
import pytest
from django.urls import reverse


from tests.helper import dict_compare_keys
from .fixtures import fixture

@pytest.mark.django_db(databases=['default'])
def test_travelperk_get_view(api_client, access_token, get_org_id, get_travelperk_id):
    """
    Test Get of Travelperk
    """
    url = reverse('travelperk:travelperk',
        kwargs={
                'org_id': get_org_id,
            }
    )

    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == 200

    response = json.loads(response.content)
    assert dict_compare_keys(response, fixture['travelperk']) == [], 'orgs GET diff in keys'

    url = reverse('travelperk:travelperk',
        kwargs={
                'org_id': 123,
            }
    )
    response = api_client.get(url)
    assert response.status_code == 404

    response = json.loads(response.content)
    assert response['message'] != None
