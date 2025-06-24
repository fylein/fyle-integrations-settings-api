"""
Mock setup for users tests.
Contains all mocking patterns used across users test files.
"""

from unittest.mock import MagicMock


def mock_get_cluster_domain(mocker):
    """
    Mock get_cluster_domain function
    """
    mock_cluster_domain = mocker.patch('apps.users.helpers.get_cluster_domain')
    mock_cluster_domain.return_value = 'https://lolo.fyle.tech'
    return mock_cluster_domain


def mock_requests_shared_mock(mocker):
    """
    Shared mock for requests used in users helpers tests
    """
    mock_requests = mocker.patch('apps.users.helpers.requests')
    mock_response = MagicMock()
    mock_requests.get.return_value = mock_response
    mock_requests.post.return_value = mock_response
    return mock_requests, mock_response 
 