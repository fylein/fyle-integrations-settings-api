"""
Mock setup for integrations tests.
Contains all mocking patterns used across integrations test files.
"""

import pytest
from unittest.mock import MagicMock

from apps.integrations.models import Integration
from apps.orgs.models import Org


def mock_get_org_id_and_name_from_access_token(mocker):
    """
    Mock get_org_id_and_name_from_access_token function
    """
    mock_get_org = mocker.patch('apps.integrations.views.get_org_id_and_name_from_access_token')
    mock_get_org.return_value = {'id': 'or3P3xJ0603e', 'name': 'Test Org'}
    return mock_get_org


def mock_post_request(mocker):
    """
    Mock post_request function
    """
    mock_post_request = mocker.patch('apps.users.helpers.post_request')
    mock_post_request.return_value = {
        'org_id': 'or3P3xJ0603e',
        'org_name': 'Test Org'
    }
    return mock_post_request


def mock_get_cluster_domain(mocker):
    """
    Mock cluster domain setting
    """
    mock_cluster_domain = mocker.patch('apps.users.helpers.get_cluster_domain')
    mock_cluster_domain.return_value = 'https://api.fyle.in'
    return mock_cluster_domain


def mock_requests_get_success(mocker):
    """
    Mock requests.get for success case
    """
    mock_requests_get = mocker.patch('requests.get')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'org': {
                'id': 'or3P3xJ0603e',
                'name': 'Test Org'
            }
        }
    }
    mock_requests_get.return_value = mock_response
    return mock_requests_get, mock_response


def mock_requests_get_failure(mocker):
    """
    Mock requests.get for failure case
    """
    mock_requests_get = mocker.patch('requests.get')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 401
    mock_response.text = 'Unauthorized'
    mock_requests_get.return_value = mock_response
    return mock_requests_get, mock_response


def mock_requests_get_unauthorized(mocker):
    """
    Mock requests.get for unauthorized case
    """
    mock_get = mocker.patch('apps.integrations.actions.requests.get')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 401
    mock_response.text = 'Unauthorized'
    mock_get.return_value = mock_response
    return mock_get, mock_response 
