"""
Mock setup functions for integrations tests
"""


def mock_get_org_id_and_name_from_access_token(mocker):
    """
    Mock get_org_id_and_name_from_access_token function
    """
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    return dummy_org_id


def mock_get_cluster_domain(mocker):
    """
    Mock get_cluster_domain function
    """
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )


def mock_test_get_integration(mocker):
    """
    Mock setup for test_get_integration
    Case: Returns correct integration data
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_get_org_id_and_name = mocker.patch(
        'apps.integrations.actions.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    
    mock_cluster_domain = mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    return {
        'get_org_id_and_name': mock_get_org_id_and_name,
        'get_cluster_domain': mock_cluster_domain,
        'org_id': dummy_org_id,
    }


def mock_test_get_org_id_and_name_from_access_token_case_1(mocker):
    """
    Mock setup for test_get_org_id_and_name_from_access_token_case_1
    Case: Valid response returns org data
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_cluster_domain = mocker.patch(
        'apps.users.helpers.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    api_mock_response = {
        'data': {
            'org': {
                'id': dummy_org_id,
                'name': 'Dummy Org'
            }
        }
    }
    mock_response.json.return_value = api_mock_response
    
    mock_requests_get = mocker.patch('apps.integrations.actions.requests.get', return_value=mock_response)
    
    return {
        'cluster_domain': mock_cluster_domain,
        'requests_get': mock_requests_get,
        'mock_response': mock_response,
        'org_id': dummy_org_id,
    }


def mock_test_get_org_id_and_name_from_access_token_case_2(mocker):
    """
    Mock setup for test_get_org_id_and_name_from_access_token_case_2
    Case: Invalid response raises exception
    """
    mock_cluster_domain = mocker.patch(
        'apps.users.helpers.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    mock_response = mocker.MagicMock()
    mock_response.status_code = 400
    
    mock_requests_get = mocker.patch('apps.integrations.actions.requests.get', return_value=mock_response)
    
    return {
        'cluster_domain': mock_cluster_domain,
        'requests_get': mock_requests_get,
        'mock_response': mock_response,
    }


def mock_test_integrations_view_post_accounting_case_1(mocker):
    """
    Mock setup for test_integrations_view_post_accounting_case_1
    Case: Create accounting integration and verify response
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_get_org_id_and_name = mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    
    mock_cluster_domain = mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    return {
        'get_org_id_and_name': mock_get_org_id_and_name,
        'get_cluster_domain': mock_cluster_domain,
        'org_id': dummy_org_id,
    }


def mock_test_integrations_view_post_case_1(mocker):
    """
    Mock setup for test_integrations_view_post_case_1
    Case: Create and update integrations
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_get_org_id_and_name = mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    
    mock_cluster_domain = mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    return {
        'get_org_id_and_name': mock_get_org_id_and_name,
        'get_cluster_domain': mock_cluster_domain,
        'org_id': dummy_org_id,
    }


def mock_test_integrations_view_get_case_1(mocker):
    """
    Mock setup for test_integrations_view_get_case_1
    Case: Get all integrations and filter by type
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_get_org_id_and_name = mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    
    mock_cluster_domain = mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    return {
        'get_org_id_and_name': mock_get_org_id_and_name,
        'get_cluster_domain': mock_cluster_domain,
        'org_id': dummy_org_id,
    }


def mock_test_integrations_view_mark_inactive_post_case_1(mocker):
    """
    Mock setup for test_integrations_view_mark_inactive_post_case_1
    Case: Mark integration as inactive
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_get_org_id_and_name = mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    
    mock_cluster_domain = mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    return {
        'get_org_id_and_name': mock_get_org_id_and_name,
        'get_cluster_domain': mock_cluster_domain,
        'org_id': dummy_org_id,
    }


def mock_test_integrations_view_patch_case_1(mocker):
    """
    Mock setup for test_integrations_view_patch_case_1
    Case: Update integration with valid data
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_get_org_id_and_name = mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    
    mock_cluster_domain = mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    return {
        'get_org_id_and_name': mock_get_org_id_and_name,
        'get_cluster_domain': mock_cluster_domain,
        'org_id': dummy_org_id,
    }


def mock_test_integrations_view_patch_case_2(mocker):
    """
    Mock setup for test_integrations_view_patch_case_2
    Case: Update integration with invalid tpa_name
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_get_org_id_and_name = mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    
    mock_cluster_domain = mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    return {
        'get_org_id_and_name': mock_get_org_id_and_name,
        'get_cluster_domain': mock_cluster_domain,
        'org_id': dummy_org_id,
    }


def mock_test_integrations_view_patch_case_3(mocker):
    """
    Mock setup for test_integrations_view_patch_case_3
    Case: Update integration with partial data
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_get_org_id_and_name = mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    
    mock_cluster_domain = mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    return {
        'get_org_id_and_name': mock_get_org_id_and_name,
        'get_cluster_domain': mock_cluster_domain,
        'org_id': dummy_org_id,
    }


def mock_integrations_shared_mock(mocker):
    """
    Shared mock setup for integrations tests
    Returns a dictionary of mocks that can be used with mock_dependencies
    """
    dummy_org_id = 'or3P3xJ0603e'
    
    mock_get_org = mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id": dummy_org_id, "name": "Dummy Org"}
    )
    
    mock_cluster_domain = mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    
    return {
        'get_org_id_and_name': mock_get_org,
        'get_cluster_domain': mock_cluster_domain,
        'org_id': dummy_org_id,
    } 
