"""
Mock setup for travelperk tests.
Contains all mocking patterns used across travelperk test files.
"""
import pytest

from apps.travelperk.actions import add_travelperk_to_integrations
from apps.travelperk.models import TravelperkAdvancedSetting
from apps.integrations.models import Integration
from apps.orgs.models import Org


def mock_platform_connector(mocker):
    """
    Mock PlatformConnector for travelperk tests
    """
    mock_connector = mocker.patch('apps.travelperk.views.PlatformConnector')
    mock_connector.return_value.connection.v1.spender.my_profile.get.return_value = {
        'data': {
            'user': {
                'email': 'janedoe@gmail.com',
                'id': '1234'
            }
        }
    }
    return mock_connector


def mock_travelperk_connector(mocker):
    """
    Mock TravelperkConnector for travelperk tests
    """
    mock_connector = mocker.patch('apps.travelperk.views.TravelperkConnector')
    mock_connector.return_value.delete_webhook_connection.return_value = {'message': 'success'}
    mock_connector.return_value.create_webhook.return_value = {'id': 123}
    
    return mock_connector


def mock_get_refresh_token(mocker):
    """
    Mock get_refresh_token_using_auth_code function
    """
    mock_get_token = mocker.patch('apps.travelperk.views.get_refresh_token_using_auth_code')
    mock_get_token.return_value = {'123e3rwer'}
    return mock_get_token


def mock_get_category_id(mocker):
    """
    Mock get_category_id function
    """
    mock_category = mocker.patch('apps.travelperk.actions.get_category_id')
    mock_category.return_value = '1234'
    return mock_category


def mock_construct_file_ids(mocker):
    """
    Mock construct_file_ids function
    """
    mock_file_ids = mocker.patch('apps.travelperk.actions.construct_file_ids')
    mock_file_ids.return_value = ['123']
    return mock_file_ids


def mock_platform_for_actions(mocker):
    """
    Mock Platform for travelperk actions
    """
    mock_connector = mocker.patch('apps.orgs.utils.Platform')
    mock_connector.return_value.v1.admin.employees.list.return_value = {
        'data': [{'user': {'email': 'johndoe@gmail.com'}}]
    }
    mock_connector.return_value.v1.admin.expenses.post.return_value = {'data': {'id': '123'}}
    
    return mock_connector


def mock_all_travelperk_dependencies(mocker):
    """
    Mock all travelperk external dependencies
    """
    mock_platform = mock_platform_connector(mocker)
    mock_travelperk = mock_travelperk_connector(mocker)
    mock_token = mock_get_refresh_token(mocker)
    mock_category = mock_get_category_id(mocker)
    mock_file_ids = mock_construct_file_ids(mocker)
    mock_platform_actions = mock_platform_for_actions(mocker)
    
    return {
        'platform_connector': mock_platform,
        'travelperk_connector': mock_travelperk,
        'refresh_token': mock_token,
        'category_id': mock_category,
        'file_ids': mock_file_ids,
        'platform_actions': mock_platform_actions
    }


def mock_org_get_exception(mocker):
    """
    Mock Org.objects.get to raise exception
    """
    mock_org = mocker.patch('apps.orgs.models.Org.objects.get')
    mock_org.side_effect = Exception('DB error')
    return mock_org


def mock_profile_mapping_exception(mocker):
    """
    Mock TravelperkProfileMapping.bulk_create_profile_mappings to raise exception
    """
    mock_mapping = mocker.patch('apps.travelperk.models.TravelperkProfileMapping.bulk_create_profile_mappings')
    mock_mapping.side_effect = Exception('Mapping error')
    return mock_mapping


def mock_platform_connector_with_profile(mocker):
    """
    Mock PlatformConnector with profile data
    """
    mock_platform = mocker.patch('apps.travelperk.views.PlatformConnector')
    mock_platform.return_value.connection.v1.spender.my_profile.get.return_value = {
        'data': {
            'user': {
                'email': 'janedoe@gmail.com',
                'id': '1234'
            }
        }
    }
    return mock_platform


def mock_travelperk_get_exception(mocker):
    """
    Mock TravelPerk.objects.get to raise exception
    """
    mock_travelperk = mocker.patch('apps.travelperk.models.TravelPerk.objects.get')
    mock_travelperk.side_effect = Exception('DoesNotExist')
    return mock_travelperk


def mock_travelperk_connector_with_validation(mocker):
    """
    Mock TravelperkConnector for validation tests
    """
    mock_connector = mocker.patch('apps.travelperk.views.TravelperkConnector')
    mock_connector.return_value.delete_webhook_connection.return_value = {'message': 'success'}
    mock_connector.return_value.create_webhook.return_value = {'id': 123}
    
    # For expired token test, make the profiles generator raise an exception
    mock_profiles_generator = mocker.MagicMock()
    
    # Create a mock iterator that raises an exception when next() is called
    mock_iterator = mocker.MagicMock()
    mock_iterator.__next__ = mocker.MagicMock(side_effect=Exception("Token expired"))
    mock_iterator.__iter__ = mocker.MagicMock(return_value=mock_iterator)
    
    mock_profiles_generator.get_all_generator.return_value = mock_iterator
    mock_connector.return_value.connection.invoice_profiles = mock_profiles_generator
    
    return mock_connector


def mock_file_operations(mocker):
    """
    Mock file download and upload operations
    """
    mock_download = mocker.patch('apps.travelperk.actions.download_file')
    mock_download.return_value = b'data'
    
    mock_upload = mocker.patch('apps.travelperk.actions.upload_to_s3_presigned_url')
    
    return {
        'download_file': mock_download,
        'upload_to_s3': mock_upload
    }


def mock_fyle_connection(mocker):
    """
    Mock Fyle connection creation
    """
    mock_platform = mocker.MagicMock()
    mock_platform.v1.admin.employees.list.return_value = {
        'data': [{'user': {'email': 'johndoe@gmail.com'}}]
    }
    mock_platform.v1.admin.expenses.post.return_value = {'data': {'id': '123'}}
    mock_platform.v1.admin.categories.list.return_value = {'count': 1, 'data': [{'id': 'cat1'}]}
    mock_platform.v1.spender.expenses.post.return_value = {'data': {'id': 'exp1'}}
    mock_platform.v1.spender.files.create_file.return_value = {'data': {'id': 'file123'}}
    mock_platform.v1.spender.files.generate_file_urls.return_value = {'data': {'upload_url': 'http://upload'}}
    mock_platform.v1.spender.expenses.attach_receipt.return_value = True
    
    mock_create_connection = mocker.patch('apps.travelperk.actions.create_fyle_connection')
    mock_create_connection.return_value = mock_platform
    
    return mock_create_connection


def mock_employee_operations(mocker):
    """
    Mock employee-related operations
    """
    mock_get_email = mocker.patch('apps.travelperk.actions.get_employee_email')
    mock_get_email.return_value = 'test@test.com'
    
    mock_construct_files = mocker.patch('apps.travelperk.actions.construct_file_ids')
    mock_construct_files.return_value = ['file123']
    
    return {
        'get_employee_email': mock_get_email,
        'construct_file_ids': mock_construct_files
    }


def mock_invoice_operations(mocker):
    """
    Mock invoice-related operations
    """
    # Mock the create_fyle_connection function to avoid FyleCredential issues
    mock_platform = mocker.MagicMock()
    mock_platform.v1.admin.expenses.post.return_value = {'data': {'id': 'exp123'}}
    mock_platform.v1.spender.expenses.post.return_value = {'data': {'id': 'exp123'}}
    
    mock_create_connection = mocker.patch('apps.travelperk.actions.create_fyle_connection')
    mock_create_connection.return_value = mock_platform
    
    # Mock the ImportedExpenseDetail.objects.update_or_create to actually create objects
    def mock_update_or_create(*args, **kwargs):
        from apps.travelperk.models import ImportedExpenseDetail
        # Create a real ImportedExpenseDetail object
        imported_expense = ImportedExpenseDetail.objects.create(
            expense_id=kwargs.get('expense_id', 'exp123'),
            org_id=kwargs.get('org_id', 1),
            is_reciept_attached=kwargs.get('is_reciept_attached', True),
            file_id=kwargs.get('file_id', 'file123')
        )
        return imported_expense, True
    
    mock_update_or_create_patch = mocker.patch('apps.travelperk.actions.ImportedExpenseDetail.objects.update_or_create')
    mock_update_or_create_patch.side_effect = mock_update_or_create
    
    # Mock other required functions
    mock_get_employee_email = mocker.patch('apps.travelperk.actions.get_employee_email')
    mock_get_employee_email.return_value = 'test@test.com'
    
    mock_construct_files = mocker.patch('apps.travelperk.actions.construct_file_ids')
    mock_construct_files.return_value = ['file123']
    
    return {
        'create_connection': mock_create_connection,
        'update_or_create': mock_update_or_create_patch,
        'get_employee_email': mock_get_employee_email,
        'construct_file_ids': mock_construct_files
    }


def mock_expense_operations(mocker):
    """
    Mock expense-related operations
    """
    # Mock the create_fyle_connection function to avoid FyleCredential issues
    mock_platform = mocker.MagicMock()
    mock_platform.v1.admin.expenses.post.return_value = {'data': {'id': 'exp123'}}
    mock_platform.v1.spender.expenses.post.return_value = {'data': {'id': 'exp123'}}
    mock_platform.v1.admin.categories.list.return_value = {'count': 1, 'data': [{'id': 'cat123'}]}
    
    mock_create_connection = mocker.patch('apps.travelperk.actions.create_fyle_connection')
    mock_create_connection.return_value = mock_platform
    
    # Mock the ImportedExpenseDetail.objects.update_or_create to actually create objects
    def mock_update_or_create(*args, **kwargs):
        from apps.travelperk.models import ImportedExpenseDetail
        # Create a real ImportedExpenseDetail object
        imported_expense = ImportedExpenseDetail.objects.create(
            expense_id=kwargs.get('expense_id', 'exp123'),
            org_id=kwargs.get('org_id', 1),
            is_reciept_attached=kwargs.get('is_reciept_attached', True),
            file_id=kwargs.get('file_id', 'file123')
        )
        return imported_expense, True
    
    mock_update_or_create_patch = mocker.patch('apps.travelperk.actions.ImportedExpenseDetail.objects.update_or_create')
    mock_update_or_create_patch.side_effect = mock_update_or_create
    
    # Mock the create_expense_in_fyle_v2 function to actually create objects
    def mock_create_expense_v2(org_id, invoice, invoice_lineitems):
        from apps.travelperk.models import ImportedExpenseDetail
        # Create a real ImportedExpenseDetail object for each line item
        for expense in invoice_lineitems:
            imported_expense = ImportedExpenseDetail.objects.create(
                expense_id='exp123',
                org_id=org_id,
                is_reciept_attached=True,
                file_id='file123'
            )
        return imported_expense
    
    mock_create_expense_v2_patch = mocker.patch('apps.travelperk.actions.create_expense_in_fyle_v2')
    mock_create_expense_v2_patch.side_effect = mock_create_expense_v2
    
    # Mock other required functions
    mock_get_employee_email = mocker.patch('apps.travelperk.actions.get_employee_email')
    mock_get_employee_email.return_value = 'test@test.com'
    
    mock_construct_files = mocker.patch('apps.travelperk.actions.construct_file_ids')
    mock_construct_files.return_value = ['file123']
    
    # Mock attach_reciept_to_expense
    mock_attach_receipt = mocker.patch('apps.travelperk.actions.attach_reciept_to_expense')
    
    return {
        'create_connection': mock_create_connection,
        'update_or_create': mock_update_or_create_patch,
        'create_expense_v2': mock_create_expense_v2_patch,
        'get_employee_email': mock_get_employee_email,
        'construct_file_ids': mock_construct_files,
        'attach_receipt': mock_attach_receipt
    }


def mock_fyle_client_id(mocker):
    """
    Mock FYLE_CLIENT_ID setting
    """
    mocker.patch('django.conf.settings.FYLE_CLIENT_ID', 'client_id')
    return 'client_id' 
