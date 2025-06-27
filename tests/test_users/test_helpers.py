import pytest
import json
from django.conf import settings
from apps.users.helpers import get_cluster_domain, post_request


def test_get_cluster_domain_case_1(mock_dependencies, api_client, mocker, access_token):
    """
    Test get_cluster_domain helper
    Case: Returns correct cluster domain
    """
    cluster_domain = get_cluster_domain('dummy_access_token')
    assert cluster_domain == 'https://lolo.fyle.tech'


def test_post_request_case_1(mock_dependencies, api_client, mocker, access_token):
    """
    Test post_request helper
    Case: Valid response returns correct data
    """
    url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer dummy_access_token'
    }
    response = post_request(url, {}, headers)
    assert response == {'cluster_domain': 'https://test.fyle.tech'}


def test_post_request_case_2(mock_dependencies, api_client, mocker, access_token):
    """
    Test post_request helper
    Case: Invalid response raises exception
    """
    url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer dummy_access_token'
    }
    with pytest.raises(Exception):
        post_request(url, {}, headers)
