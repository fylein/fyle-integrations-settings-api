import json

import pytest
from unittest.mock import MagicMock, patch

from apps.integrations.actions import get_integration, get_org_id_name_from_access_token

from .fixture import post_integration_hrms


@pytest.mark.django_db(databases=['default'])
def test_get_integration(mocker, access_token, create_integrations):
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.actions.get_org_id_name_from_access_token',
        return_value=(dummy_org_id, "Dummy Org")
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )

    integration = get_integration('HRMS', access_token).first()

    assert integration.org_id == dummy_org_id
    assert integration.tpa_id == post_integration_hrms['tpa_id']
    assert integration.tpa_name == post_integration_hrms['tpa_name']
    assert integration.type == post_integration_hrms['type']
    assert integration.is_active == post_integration_hrms['is_active']
    assert integration.is_beta == True
    assert integration.disconnected_at == None


@pytest.mark.django_db(databases=['default'])
@patch('apps.integrations.actions.requests')
def test_get_org_id_name_from_access_token(api_client, mocker, access_token, create_integrations):
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.users.helpers.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )

    mock_response = MagicMock()
    mock_response.status_code = 200

    api_mock_response = {
        'data': {
            'org': {
                'id': dummy_org_id,
                'name': 'Dummy Org'
            }
        }
    }

    mock_response.text = json.dumps(api_mock_response)

    api_client.get.return_value = mock_response

    get_org_id_name_from_access_token(access_token)

    mock_response = MagicMock()
    mock_response.status_code = 400
    api_client.get.return_value = mock_response

    with pytest.raises(Exception):
        get_org_id_name_from_access_token(access_token)
