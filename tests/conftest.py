import uuid
from unittest import mock
from datetime import datetime, timezone
import pytest
from fyle_rest_auth.models import User, AuthToken
from rest_framework.test import APIClient
from admin_settings import settings
import json
import importlib
from pathlib import Path

from tests.fixture import fixture
from tests.test_bamboohr.fixtures import fixture as bamboohr_fixture
from tests.test_travelperk.fixtures import fixture as travelperk_fixture
from tests.test_integrations.fixture import post_integration_accounting, post_integration_hrms
from tests.test_orgs.fixtures import fixture as orgs_fixture
from apps.orgs.models import (
    Org,
    FyleCredential
)
from apps.bamboohr.models import (
    BambooHr,
    BambooHrConfiguration
)
from apps.travelperk.models import (
    TravelPerk,
    TravelperkProfileMapping,
    TravelperkAdvancedSetting,
    TravelperkCredential,
    Invoice,
    InvoiceLineItem
)
from apps.integrations.models import Integration


@pytest.fixture()
def api_client():
    """
    Create API client for testing
    """
    return APIClient()


@pytest.fixture(scope="session", autouse=True)
def default_session_fixture(request):
    """
    Session-level mocks for authentication and external services
    """
    patched_1 = mock.patch(
        'fyle_rest_auth.authentication.get_fyle_admin',
        return_value=fixture['my_profile']
    )
    patched_1.__enter__()

    patched_2 = mock.patch(
        'fyle.platform.internals.auth.Auth.update_access_token',
        return_value='abcd'
    )
    patched_2.__enter__()

    patched_3 = mock.patch(
        'apps.users.helpers.post_request',
        return_value={
            'access_token': 'abcd.efgh.jklm',
            'cluster_domain': 'https://lolo.fyle.tech'
        }
    )
    patched_3.__enter__()

    patched_4 = mock.patch(
        'fyle.platform.apis.v1.spender.MyProfile.get',
        return_value=fixture['my_profile']
    )
    patched_4.__enter__()

    patched_5 = mock.patch(
        'apps.users.helpers.get_cluster_domain',
        return_value='https://lolo.fyle.tech'
    )
    patched_5.__enter__()

    patched_6 = mock.patch(
        'fyle_rest_auth.helpers.get_fyle_admin',
        return_value=fixture['my_profile']
    )
    patched_6.__enter__()


@pytest.fixture()
def access_token(db):
    """
    Create access token for authentication
    """
    create_user_and_tokens()
    return 'abcd.efgh.jklm'


def create_user_and_tokens():
    """
    Create test users and tokens
    """
    user = create_user('ashwin.t@fyle.in', 'Joanna', 'usqywo0f3nBY')
    create_auth_token(user)

    org = Org.objects.create(
        name='Anagha Org', fyle_org_id='orHVw3ikkCxJ', cluster_domain='https://lolo.fyle.tech'
    )
    org.user.add(user)
    FyleCredential.objects.create(
        refresh_token=settings.FYLE_REFRESH_TOKEN,
        org=org,
    )

    user = create_user('ashwin.t+1@fyle.in', 'Joannaa', 'usqywo0f3nBZ')
    create_auth_token(user)


def create_user(email: str, name: str, user_id: str) -> User:
    """
    Create a test user
    """
    return User.objects.create(
        password='', last_login=datetime.now(tz=timezone.utc), email=email,
        user_id=user_id, full_name=name, active='t', staff='f', admin='f'
    )


def create_auth_token(user: User):
    """
    Create auth token for user
    """
    AuthToken.objects.create(
        refresh_token='refresh_token',
        user=user
    )


@pytest.fixture()
def org_data():
    """
    Test data for organization creation
    """
    return {
        'name': 'Test Organization',
        'fyle_org_id': f'orTwovfDpEYc_{uuid.uuid4()}',
        'managed_user_id': '890744',
        'cluster_domain': 'https://fake-cluster-domain.com',
    }


@pytest.fixture()
def fyle_credential_data():
    """
    Test data for Fyle credential creation
    """
    return {
        'refresh_token': 'fake-refresh-token',
    }


@pytest.fixture()
def create_org(org_data, fyle_credential_data, db):
    """
    Create a test organization with Fyle credentials
    """
    org = Org.objects.create(**org_data)
    FyleCredential.objects.create(
        org=org,
        **fyle_credential_data
    )
    return org


@pytest.fixture()
def bamboohr_data():
    """
    Test data for BambooHR creation
    """
    return {
        'folder_id': bamboohr_fixture['bamboohr']['folder_id'],
        'package_id': bamboohr_fixture['bamboohr']['package_id'],
    }


@pytest.fixture()
def create_bamboohr(create_org, bamboohr_data, db):
    """
    Create a test BambooHR instance with configuration
    """
    bamboohr = BambooHr.objects.create(
        org=create_org,
        **bamboohr_data
    )
    BambooHrConfiguration.objects.create(
        org=create_org
    )
    return bamboohr


@pytest.fixture()
def travelperk_data():
    """
    Test data for TravelPerk creation
    """
    return {
        'folder_id': travelperk_fixture['travelperk']['folder_id'],
        'package_id': travelperk_fixture['travelperk']['package_id'],
        'is_travelperk_connected': True,
    }


@pytest.fixture()
def create_travelperk(create_org, travelperk_data, db):
    """
    Create a test TravelPerk instance
    """
    return TravelPerk.objects.create(
        org=create_org,
        **travelperk_data
    )


@pytest.fixture()
def travelperk_profile_mapping_data():
    """
    Test data for TravelPerk profile mapping creation
    """
    mapping = travelperk_fixture['profile_mapping']['results'][0]
    return {
        'profile_name': mapping['profile_name'],
        'user_role': mapping['user_role'],
        'is_import_enabled': mapping['is_import_enabled'],
        'source_id': mapping['source_id'],
        'currency': mapping['currency']
    }


@pytest.fixture()
def create_travelperk_profile_mapping(create_org, travelperk_profile_mapping_data, db):
    """
    Create a test TravelPerk profile mapping
    """
    return TravelperkProfileMapping.objects.create(
        org=create_org,
        **travelperk_profile_mapping_data
    )


@pytest.fixture()
def travelperk_advanced_setting_data():
    """
    Test data for TravelPerk advanced setting creation
    """
    return {
        'default_employee_name': travelperk_fixture['advance_setting_payload']['default_employee_name'],
        'default_employee_id': travelperk_fixture['advance_setting_payload']['default_employee_id'],
        'default_category_name': travelperk_fixture['advance_setting_payload']['default_category_name'],
        'default_category_id': travelperk_fixture['advance_setting_payload']['default_category_id'],
        'invoice_lineitem_structure': travelperk_fixture['advance_setting_payload']['invoice_lineitem_structure'],
        'description_structure': travelperk_fixture['advance_setting_payload']['description_structure'],
        'category_mappings': travelperk_fixture['advance_setting_payload']['category_mappings'],
    }


@pytest.fixture()
def create_travelperk_advanced_setting(create_org, travelperk_advanced_setting_data, db):
    """
    Create a test TravelPerk advanced setting
    """
    return TravelperkAdvancedSetting.objects.create(
        org=create_org,
        **travelperk_advanced_setting_data
    )


@pytest.fixture()
def travelperk_credential_data():
    """
    Test data for TravelPerk credential creation
    """
    return {
        'refresh_token': '12312rwer',
    }


@pytest.fixture()
def create_travelperk_credential(create_org, travelperk_credential_data, db):
    """
    Create a test TravelPerk credential
    """
    return TravelperkCredential.objects.create(
        org=create_org,
        **travelperk_credential_data
    )


@pytest.fixture()
def create_invoice_and_invoice_lineitems(create_org, db):
    """
    Create test invoice and invoice line items
    """
    data = fixture['expense']
    invoice_lineitems_data = data['lines']

    invoice = Invoice.create_or_update_invoices(data, create_org.id)
    invoice_lineitems = InvoiceLineItem.create_or_update_invoice_lineitems(invoice_lineitems_data, invoice)

    return invoice, invoice_lineitems


@pytest.fixture()
def integration_accounting_data():
    """
    Test data for accounting integration creation
    """
    return {
        'org_id': post_integration_accounting.get('org_id', 'or3P3xJ0603e'),
        'type': post_integration_accounting['type'],
        'is_active': post_integration_accounting['is_active'],
        'is_beta': True,
        'tpa_id': post_integration_accounting['tpa_id'],
        'tpa_name': post_integration_accounting['tpa_name'],
    }


@pytest.fixture()
def integration_hrms_data():
    """
    Test data for HRMS integration creation
    """
    return {
        'org_id': post_integration_hrms.get('org_id', 'or3P3xJ0603e'),
        'type': post_integration_hrms['type'],
        'is_active': post_integration_hrms['is_active'],
        'is_beta': True,
        'tpa_id': post_integration_hrms['tpa_id'],
        'tpa_name': post_integration_hrms['tpa_name'],
    }


@pytest.fixture()
def create_integrations(integration_accounting_data, integration_hrms_data, db):
    """
    Create test integrations for testing
    """
    Integration.objects.create(**integration_accounting_data)
    Integration.objects.create(**integration_hrms_data)


def pytest_configure(config):
    """
    Register custom markers
    """
    config.addinivalue_line(
        "markers", "shared_mocks: mark test to use shared mock dependencies"
    )


def pytest_runtest_setup(item):
    """
    Setup shared mocks before test execution
    """
    shared_mocks_marker = item.get_closest_marker("shared_mocks")
    if shared_mocks_marker:
        item._mock_setup_func = shared_mocks_marker.args[0]


def load_mock_function(function_name, test_path):
    """
    Load a mock function dynamically from the appropriate mock_setup.py file based on the test's app folder.
    Always looks for tests.{app_name}.mock_setup.
    :param function_name: The name of the mock function to load
    :param test_path: The path to the test file
    :return: The mock function if found, otherwise None
    """
    try:
        # Convert to Path object and find the tests directory
        path = Path(test_path)
        path_parts = path.parts
        
        # Find the index of 'tests' in the path
        try:
            tests_index = path_parts.index('tests')
            # Get the app name (the folder after 'tests')
            app_name = path_parts[tests_index + 1]
        except (ValueError, IndexError):
            print(f"Could not find 'tests' directory in path: {test_path}")
            return None

        # Construct the mock_setup module path for the app
        mock_setup_module = f"tests.{app_name}.mock_setup"

        # Dynamically import the mock_setup module
        module = importlib.import_module(mock_setup_module)
        print(f"Loaded module {mock_setup_module} for test {test_path}")

        # Retrieve and return the function, or None if it doesn't exist
        return getattr(module, function_name, None)
    except (ModuleNotFoundError, IndexError) as e:
        print(f"Error: Could not load module {mock_setup_module}. Exception: {e}")
        return None


@pytest.fixture()
def mock_dependencies(request, mocker):
    """
    Fixture to apply shared and test-specific mocks.
    Shared mocks are provided via a decorator, while test-specific mocks follow a naming convention.
    """
    class MockContainer:
        pass

    mock_container = MockContainer()

    # Apply shared mocks from the decorator
    shared_mocks_marker = request.node.get_closest_marker("shared_mocks")
    if shared_mocks_marker:
        for mock_func in shared_mocks_marker.args:
            shared_mocks = mock_func(mocker)
            for key, value in shared_mocks.items():
                setattr(mock_container, key, value)

    # Apply test-specific mocks based on test's location
    test_method_name = request.node.name
    test_specific_mock_name = f"mock_{test_method_name}"

    # Get the test file path for dynamic loading
    test_file_path = request.node.fspath

    # Dynamically load the appropriate mock function from the correct mock_setup.py
    test_specific_mock_function = load_mock_function(test_specific_mock_name, test_file_path)

    if test_specific_mock_function:
        test_specific_mocks = test_specific_mock_function(mocker)
        for key, value in test_specific_mocks.items():
            setattr(mock_container, key, value)
    else:
        print(f"Test-specific mock function not found: {test_specific_mock_name}")

    return mock_container
