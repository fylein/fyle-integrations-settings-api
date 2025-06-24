import pytest
from apps.orgs.utils import create_fyle_connection, import_categories
from tests.test_orgs.mock_setup import mock_fyle_platform_shared_mock, mock_platform_connector_sync_categories_shared_mock


@pytest.mark.shared_mocks(lambda mocker: mock_fyle_platform_shared_mock(mocker))
def test_create_fyle_connection_case_1(mock_dependencies, add_org_with_credentials, db):
    """
    Test create_fyle_connection function
    """
    # Test creating Fyle connection
    result = create_fyle_connection(add_org_with_credentials.id)
    
    # Verify the function returns a connection
    assert result is not None


@pytest.mark.shared_mocks(lambda mocker: mock_platform_connector_sync_categories_shared_mock(mocker))
def test_import_categories_case_1(mock_dependencies, add_org_with_credentials, db):
    """
    Test import_categories function
    """
    # Test importing categories
    result = import_categories(add_org_with_credentials.id)
    
    # Verify the function was called and returns empty list
    assert result == []
