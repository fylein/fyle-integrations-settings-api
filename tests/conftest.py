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

from tests.fixture import (
    fixture, 
    org_data as static_org_data, 
    fyle_credential_data as static_fyle_credential_data, 
    bamboohr_data as static_bamboohr_data,
    bamboohr_configuration_data as static_bamboohr_configuration_data,
    travelperk_data as static_travelperk_data,
    travelperk_profile_mapping_data as static_travelperk_profile_mapping_data,
    travelperk_advanced_setting_data as static_travelperk_advanced_setting_data,
    travelperk_credential_data as static_travelperk_credential_data,
    integration_accounting_data as static_integration_accounting_data,
    integration_hrms_data as static_integration_hrms_data
)
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
from apps.fyle_hrms_mappings.models import DestinationAttribute, ExpenseAttribute
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
def create_org(db):
    """
    Create a test organization with Fyle credentials
    """
    org = Org.objects.create(**static_org_data)
    FyleCredential.objects.create(
        org=org,
        **static_fyle_credential_data
    )
    return org


@pytest.fixture()
def create_bamboohr(create_org):
    """
    Create a test BambooHR instance with configuration
    """
    bamboohr = BambooHr.objects.create(
        org=create_org,
        **static_bamboohr_data
    )
    BambooHrConfiguration.objects.create(
        org=create_org
    )
    return bamboohr


@pytest.fixture()
def create_bamboohr_configuration(create_org):
    """
    Create a test BambooHR configuration
    """
    return BambooHrConfiguration.objects.create(
        org=create_org,
        **static_bamboohr_configuration_data
    )


@pytest.fixture()
def create_destination_attributes(create_org):
    """
    Create test DestinationAttribute records for employee data
    """
    attributes = [
        DestinationAttribute.objects.create(
            org_id=create_org.id,
            attribute_type='EMPLOYEE',
            value='John Doe',
            destination_id='123',
            detail={
                'email': 'john.doe@example.com',
                'full_name': 'John Doe',
                'department_name': 'Engineering',
                'approver_emails': ['supervisor@example.com']
            },
            active=True,
            is_failure_email_sent=False
        ),
        DestinationAttribute.objects.create(
            org_id=create_org.id,
            attribute_type='EMPLOYEE',
            value='Jane Smith',
            destination_id='456',
            detail={
                'email': None,
                'full_name': 'Jane Smith',
                'department_name': 'Marketing',
                'approver_emails': [None]
            },
            active=True,
            is_failure_email_sent=False
        )
    ]
    return attributes


@pytest.fixture()
def create_expense_attribute(create_org):
    """
    Create an ExpenseAttribute for testing
    """
    from tests.test_fyle_employee_imports.fixtures import expense_attribute_data
    
    return ExpenseAttribute.objects.create(
        org_id=create_org.id,
        **expense_attribute_data
    )


@pytest.fixture()
def create_travelperk(create_org):
    """
    Create a test TravelPerk instance
    """
    return TravelPerk.objects.create(
        org=create_org,
        **static_travelperk_data
    )


@pytest.fixture()
def create_travelperk_profile_mapping(create_org):
    """
    Create a test TravelPerk profile mapping
    """
    return TravelperkProfileMapping.objects.create(
        org=create_org,
        **static_travelperk_profile_mapping_data
    )


@pytest.fixture()
def create_travelperk_advanced_setting(create_org):
    """
    Create a test TravelPerk advanced setting
    """
    return TravelperkAdvancedSetting.objects.create(
        org=create_org,
        **static_travelperk_advanced_setting_data
    )


@pytest.fixture()
def create_travelperk_credential(create_org):
    """
    Create a test TravelPerk credential
    """
    return TravelperkCredential.objects.create(
        org=create_org,
        **static_travelperk_credential_data
    )


@pytest.fixture()
def create_invoice_and_invoice_lineitems(create_org):
    """
    Create test invoice and invoice line items
    """
    data = fixture['expense']
    invoice_lineitems_data = data['lines']

    invoice = Invoice.create_or_update_invoices(data, create_org.id)
    invoice_lineitems = InvoiceLineItem.create_or_update_invoice_lineitems(invoice_lineitems_data, invoice)

    return invoice, invoice_lineitems


@pytest.fixture()
def create_integrations(db):
    """
    Create test integrations for testing
    """
    Integration.objects.create(**static_integration_accounting_data)
    Integration.objects.create(**static_integration_hrms_data)


@pytest.fixture()
def create_travelperk_full_setup(create_org):
    """
    Create a complete TravelPerk setup with all dependencies
    """
    travelperk = TravelPerk.objects.create(
        org=create_org,
        **static_travelperk_data
    )
    
    travelperk_credential = TravelperkCredential.objects.create(
        org=create_org,
        **static_travelperk_credential_data
    )
    
    travelperk_advanced_setting = TravelperkAdvancedSetting.objects.create(
        org=create_org,
        **static_travelperk_advanced_setting_data
    )
    
    travelperk_profile_mapping = TravelperkProfileMapping.objects.create(
        org=create_org,
        **static_travelperk_profile_mapping_data
    )
    
    data = fixture['expense']
    invoice_lineitems_data = data['lines']
    invoice = Invoice.create_or_update_invoices(data, create_org.id)
    invoice_lineitems = InvoiceLineItem.create_or_update_invoice_lineitems(invoice_lineitems_data, invoice)
    
    return {
        'org': create_org,
        'travelperk': travelperk,
        'credential': travelperk_credential,
        'advanced_setting': travelperk_advanced_setting,
        'profile_mapping': travelperk_profile_mapping,
        'invoice': invoice,
        'invoice_lineitems': invoice_lineitems
    }


@pytest.fixture()
def create_bamboohr_full_setup(create_org):
    """
    Create a complete BambooHR setup with all dependencies
    """
    # FyleCredential is already created by create_org fixture
    fyle_credential = FyleCredential.objects.get(org=create_org)
    
    bamboohr = BambooHr.objects.create(
        org=create_org,
        **static_bamboohr_data
    )
    
    bamboohr_config = BambooHrConfiguration.objects.create(
        org=create_org,
        **static_bamboohr_configuration_data
    )
    
    return {
        'org': create_org,
        'bamboohr': bamboohr,
        'config': bamboohr_config,
        'fyle_credential': fyle_credential
    }


@pytest.fixture()
def create_employee_missing_email(create_org):
    """
    Create a destination attribute for employee with missing email
    """
    return DestinationAttribute.objects.create(
        org_id=create_org.id,
        attribute_type='EMPLOYEE',
        value='Test Employee',
        destination_id='999',
        detail={
            'email': None,
            'full_name': 'Test Employee',
            'department_name': 'Test Department',
            'approver_emails': [None]
        },
        active=True,
        is_failure_email_sent=False
    )


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
