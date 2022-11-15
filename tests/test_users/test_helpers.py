import pytest
import json
from unittest.mock import MagicMock, patch

from django.conf import settings

from apps.users.helpers import get_cluster_domain, post_request

@pytest.mark.django_db(databases=['default'])
def test_get_cluster_domain_request(api_client, mocker, access_token):
    dummy_cluster_domain = 'https://lolo.fyle.tech'
    mocker.patch(
        'apps.users.helpers.post_request',
        return_value={
            'cluster_domain': dummy_cluster_domain
        }
    )

    cluster_domain = get_cluster_domain('dummy_access_token')
    assert cluster_domain == dummy_cluster_domain


@pytest.mark.django_db(databases=['default'])
@patch('apps.users.helpers.requests')
def test_post_request(api_client, mocker, access_token):
    url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)

    mock_response = MagicMock()
    mock_response.status_code = 200

    api_mock_response = {
        'access_token': 'abcd.efgh.jklm',
        'cluster_domain': 'https://lolo.fyle.tech'
    }

    mock_response.text = json.dumps(api_mock_response)

    api_client.post.return_value = mock_response

    response = post_request(url, {}, 'dummy_access_token')
    assert response == api_mock_response

    mock_response = MagicMock()
    mock_response.status_code = 400
    api_client.post.return_value = mock_response

    with pytest.raises(Exception):
        post_request(url, {}, 'dummy_access_token')
