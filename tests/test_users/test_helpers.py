import pytest
import json
from unittest.mock import MagicMock
from django.conf import settings
from apps.users.helpers import post_request, get_cluster_domain
from tests.test_users.mock_setup import mock_requests_shared_mock


def test_get_cluster_domain_request(api_client, mocker, access_token, db):
    url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)

    mock_requests, mock_response = mock_requests_shared_mock(mocker)
    mock_response.status_code = 200

    api_mock_response = {
        'access_token': 'abcd.efgh.jklm',
        'cluster_domain': 'https://lolo.fyle.tech'
    }

    mock_response.text = json.dumps(api_mock_response)

    mock_requests.post.return_value = mock_response

    response = get_cluster_domain('dummy_access_token')
    assert response == 'https://lolo.fyle.tech'


def test_post_request(api_client, mocker, access_token, db):
    url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)

    mock_requests, mock_response = mock_requests_shared_mock(mocker)
    mock_response.status_code = 200

    api_mock_response = {
        'access_token': 'abcd.efgh.jklm',
        'cluster_domain': 'https://lolo.fyle.tech'
    }

    mock_response.text = json.dumps(api_mock_response)

    # Mock the requests.post method properly
    mock_requests.post.return_value = mock_response

    api_headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer dummy_access_token'
    }

    response = post_request(url, {}, api_headers)
    assert response == api_mock_response

    # Test error case
    mock_response_error = MagicMock()
    mock_response_error.status_code = 400
    mock_requests.post.return_value = mock_response_error

    with pytest.raises(Exception):
        post_request(url, {}, api_headers)
