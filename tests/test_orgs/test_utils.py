import pytest
from apps.orgs.utils import import_categories, create_fyle_connection
from apps.users.helpers import PlatformConnector
from django.core.exceptions import ObjectDoesNotExist
from unittest.mock import patch
from .mock_setup import mock_test_import_categories_success, mock_test_create_fyle_connection_success

@pytest.mark.shared_mocks(lambda mocker: mock_test_import_categories_success(mocker))
def test_import_categories_success(mock_dependencies, create_org):
    """
    Test import_categories returns categories from PlatformConnector
    """
    with patch('apps.orgs.utils.PlatformConnector', return_value=mock_dependencies.platform_connector):
        categories = import_categories(create_org.id)
    assert categories == mock_dependencies.expected_categories
    mock_dependencies.platform_connector.sync_categories.assert_called_once_with(org_id=create_org.id)


def test_import_categories_org_not_found(mock_dependencies, db):
    """
    Test import_categories raises ObjectDoesNotExist if Org does not exist
    """
    with pytest.raises(ObjectDoesNotExist):
        import_categories(999999)


@pytest.mark.shared_mocks(lambda mocker: mock_test_create_fyle_connection_success(mocker))
def test_create_fyle_connection_success(mock_dependencies, create_org, settings):
    """
    Test create_fyle_connection returns a Platform instance with correct params
    """
    with patch('apps.orgs.utils.Platform', mock_dependencies.platform_class):
        connection = create_fyle_connection(create_org.id)
    assert connection == mock_dependencies.platform_instance
    mock_dependencies.platform_class.assert_called_once()


def test_create_fyle_connection_credential_not_found(mock_dependencies, create_org, db):
    """
    Test create_fyle_connection raises ObjectDoesNotExist if FyleCredential does not exist
    """
    with pytest.raises(ObjectDoesNotExist):
        create_fyle_connection(999999)
