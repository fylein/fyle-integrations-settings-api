import pytest
from unittest.mock import MagicMock, patch


def mock_test_get_cluster_domain_case_1(mocker):
    """
    Mock setup for test_get_cluster_domain_case_1
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"cluster_domain": "https://test.fyle.tech"}'
    
    mock_post = mocker.patch('apps.users.helpers.requests.post', return_value=mock_response)
    return mock_post


def mock_test_post_request_case_1(mocker):
    """
    Mock setup for test_post_request_case_1
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"cluster_domain": "https://test.fyle.tech"}'
    
    mock_post = mocker.patch('apps.users.helpers.requests.post', return_value=mock_response)
    return mock_post


def mock_test_post_request_case_2(mocker):
    """
    Mock setup for test_post_request_case_2
    """
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = 'Bad Request'
    
    mock_post = mocker.patch('apps.users.helpers.requests.post', return_value=mock_response)
    return mock_post 
