import json
import pytest
from rest_framework import status

from apps.integrations.actions import get_integration, get_org_id_and_name_from_access_token
from apps.integrations.models import Integration
from apps.orgs.models import Org
from tests.helper import dict_compare_keys
from .fixture import post_integration_hrms
from .mock_setup import (
    mock_get_org_id_and_name_from_access_token,
    mock_get_cluster_domain,
    mock_requests_get_success,
    mock_requests_get_failure,
    mock_requests_get_unauthorized
)


def test_get_integration_success(mocker, access_token, create_integrations, db):
    """
    Test get_integration function
    Case: successful integration retrieval
    """
    dummy_org_id = 'or3P3xJ0603e'
    # Mock both cluster domain and requests.get
    mock_get_cluster_domain(mocker)
    mock_requests_get_success(mocker)

    integration = get_integration('HRMS', access_token).first()

    assert integration.org_id == dummy_org_id
    assert integration.tpa_id == post_integration_hrms['tpa_id']
    assert integration.tpa_name == post_integration_hrms['tpa_name']
    assert integration.type == post_integration_hrms['type']
    assert integration.is_active == post_integration_hrms['is_active']
    assert integration.is_beta == True
    assert integration.disconnected_at == None


def test_get_org_id_and_name_from_access_token_success(mocker, access_token, create_integrations, db):
    """
    Test get_org_id_and_name_from_access_token function
    Case: successful token validation
    """
    dummy_org_id = 'or3P3xJ0603e'
    mock_cluster_domain = mock_get_cluster_domain(mocker)
    mock_requests, mock_response = mock_requests_get_success(mocker)

    get_org_id_and_name_from_access_token(access_token)

    # Test failure case
    mock_requests_failure, mock_response_failure = mock_requests_get_failure(mocker)

    with pytest.raises(Exception):
        get_org_id_and_name_from_access_token(access_token)


def test_get_org_id_and_name_from_access_token_error(mocker):
    """
    Test get_org_id_and_name_from_access_token function
    Case: error with response text if status is not 200
    """
    # Use shared mock for unauthorized case
    mock_get, mock_response = mock_requests_get_unauthorized(mocker)
    
    with pytest.raises(Exception) as exc:
        get_org_id_and_name_from_access_token('bad_token')
    assert 'Unauthorized' in str(exc.value)
