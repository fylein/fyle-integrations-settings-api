import json
import pytest
from unittest.mock import MagicMock

from apps.integrations.actions import get_integration, get_org_id_and_name_from_access_token
from .fixture import post_integration_hrms


def test_get_integration(mock_dependencies, mocker, access_token, create_integrations, db):
    """
    Test get_integration action
    Case: Returns correct integration data
    """
    integration = get_integration('HRMS', access_token).first()

    assert integration.org_id == mock_dependencies.org_id
    assert integration.tpa_id == post_integration_hrms['tpa_id']
    assert integration.tpa_name == post_integration_hrms['tpa_name']
    assert integration.type == post_integration_hrms['type']
    assert integration.is_active == post_integration_hrms['is_active']
    assert integration.is_beta is True
    assert integration.disconnected_at is None


def test_get_org_id_and_name_from_access_token_case_1(mock_dependencies, api_client, mocker, access_token, create_integrations, db):
    """
    Test get_org_id_and_name_from_access_token action
    Case: Valid response returns org data
    """
    result = get_org_id_and_name_from_access_token(access_token)
    assert result['id'] == mock_dependencies.org_id
    assert result['name'] == 'Dummy Org'


def test_get_org_id_and_name_from_access_token_case_2(mock_dependencies, api_client, mocker, access_token, create_integrations, db):
    """
    Test get_org_id_and_name_from_access_token action
    Case: Invalid response raises exception
    """
    with pytest.raises(Exception):
        get_org_id_and_name_from_access_token(access_token)
