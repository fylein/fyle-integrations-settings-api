"""
Mock setup for fyle_employee_imports tests.
Contains all mocking patterns used across fyle_employee_imports test files.
"""

import pytest
from unittest.mock import MagicMock

from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.orgs.models import Org, FyleCredential
from apps.fyle_hrms_mappings.models import DestinationAttribute, ExpenseAttribute


def mock_bamboo_hr_sdk(mocker):
    """
    Mock BambooHR SDK for employee imports
    """
    mock_sdk = MagicMock()
    mock_sdk.employees.get.return_value = {
        'employees': [
            {
                'id': 1,
                'firstName': 'John',
                'lastName': 'Doe',
                'workEmail': 'john.doe@example.com',
                'jobTitle': 'Software Engineer',
                'department': 'Engineering'
            },
            {
                'id': 2,
                'firstName': 'Jane',
                'lastName': 'Smith',
                'workEmail': 'jane.smith@example.com',
                'jobTitle': 'Product Manager',
                'department': 'Product'
            }
        ]
    }
    
    mock_bamboo_hr_sdk = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK')
    mock_bamboo_hr_sdk.return_value = mock_sdk
    return mock_bamboo_hr_sdk, mock_sdk


def mock_platform_connector(mocker):
    """
    Mock PlatformConnector for employee imports
    """
    mock_platform = MagicMock()
    mock_platform.sync_employees.return_value = None
    mock_platform.get_department_generator.return_value = []
    mock_platform.post_department.return_value = None
    mock_platform.bulk_post_employees.return_value = None
    mock_platform.get_employee_by_email.return_value = []
    
    mock_platform_connector = mocker.patch('fyle_employee_imports.base.PlatformConnector')
    mock_platform_connector.return_value = mock_platform
    return mock_platform_connector, mock_platform


def mock_fyle_platform(mocker):
    """
    Mock Fyle Platform for employee imports
    """
    mock_platform = MagicMock()
    mock_platform.v1.admin.employees.post.return_value = {
        'data': {
            'id': 'emp_123',
            'email': 'john.doe@example.com',
            'full_name': 'John Doe'
        }
    }
    
    mock_fyle_platform = mocker.patch('fyle_employee_imports.bamboo_hr.Platform')
    mock_fyle_platform.return_value = mock_platform
    return mock_fyle_platform, mock_platform


def mock_all_fyle_employee_imports_dependencies(mocker):
    """
    Mock all fyle_employee_imports external dependencies
    """
    mock_bamboo_hr = mock_bamboo_hr_sdk(mocker)
    mock_fyle = mock_fyle_platform(mocker)
    mock_platform = mock_platform_connector(mocker)
    
    return {
        'bamboo_hr_sdk': mock_bamboo_hr,
        'fyle_platform': mock_fyle,
        'platform_connector': mock_platform
    }


def mock_fyle_platform_employee_api(mocker):
    """
    Mock Fyle platform employee API calls
    """
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'employees': [
                {'id': 1, 'full_name': 'John Doe', 'email': 'john@example.com'},
                {'id': 2, 'full_name': 'Jane Smith', 'email': 'jane@example.com'}
            ]
        }
    }
    
    mock_requests = mocker.patch('requests.get')
    mock_requests.return_value = mock_response
    
    return mock_requests, mock_response


def mock_fyle_platform_department_api(mocker):
    """
    Mock Fyle platform department API calls
    """
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'departments': [
                {'id': 1, 'name': 'Engineering'},
                {'id': 2, 'name': 'Marketing'}
            ]
        }
    }
    
    mock_requests = mocker.patch('requests.post')
    mock_requests.return_value = mock_response
    
    return mock_requests, mock_response


def mock_hrms_employee_api(mocker):
    """
    Mock HRMS employee API calls
    """
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'employees': [
                {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
                {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
            ]
        }
    }
    
    mock_requests = mocker.patch('requests.get')
    mock_requests.return_value = mock_response
    
    return mock_requests, mock_response


def mock_all_employee_import_dependencies(mocker):
    """
    Mock all employee import external dependencies
    """
    mock_fyle_employees = mock_fyle_platform_employee_api(mocker)
    mock_fyle_departments = mock_fyle_platform_department_api(mocker)
    mock_hrms_employees = mock_hrms_employee_api(mocker)
    
    return {
        'fyle_employees': mock_fyle_employees,
        'fyle_departments': mock_fyle_departments,
        'hrms_employees': mock_hrms_employees
    }


def mock_org_objects_get(mocker, mock_org):
    """
    Mock Org.objects.get
    """
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get')
    mock_org_get.return_value = mock_org
    return mock_org_get


def mock_org_objects_get_exception(mocker):
    """
    Mock Org.objects.get to raise exception
    """
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get')
    mock_org_get.side_effect = Exception('Org not found')
    return mock_org_get


def mock_fyle_credential_objects_get(mocker, mock_credential):
    """
    Mock FyleCredential.objects.get
    """
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get')
    mock_credential_get.return_value = mock_credential
    return mock_credential_get


def mock_fyle_credential_objects_get_exception(mocker):
    """
    Mock FyleCredential.objects.get to raise exception
    """
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get')
    mock_credential_get.side_effect = Exception('Credential not found')
    return mock_credential_get


def mock_bamboo_hr_objects_filter(mocker, mock_queryset):
    """
    Mock BambooHr.objects.filter
    """
    mock_filter = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHr.objects.filter')
    mock_filter.return_value = mock_queryset
    return mock_filter


def mock_bamboo_hr_configuration_objects_get(mocker, mock_configuration):
    """
    Mock BambooHrConfiguration.objects.get
    """
    mock_config_get = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrConfiguration.objects.get')
    mock_config_get.return_value = mock_configuration
    return mock_config_get


def mock_bamboo_hr_configuration_objects_get_exception(mocker):
    """
    Mock BambooHrConfiguration.objects.get to raise exception
    """
    mock_config_get = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrConfiguration.objects.get')
    mock_config_get.side_effect = Exception('BambooHrConfiguration.DoesNotExist')
    return mock_config_get


def mock_importer_upsert_employees(mocker, importer):
    """
    Mock importer.upsert_employees method
    """
    mock_upsert = mocker.patch.object(importer, 'upsert_employees')
    return mock_upsert


def mock_importer_get_admin_email(mocker, importer):
    """
    Mock importer.get_admin_email method
    """
    mock_admin_email = mocker.patch.object(importer, 'get_admin_email')
    mock_admin_email.return_value = ['admin@test.com']
    return mock_admin_email


def mock_importer_get_existing_departments(mocker, importer):
    """
    Mock importer.get_existing_departments_from_fyle method
    """
    mock_departments = mocker.patch.object(importer, 'get_existing_departments_from_fyle')
    mock_departments.return_value = {}
    return mock_departments


def mock_importer_create_department_payload(mocker, importer):
    """
    Mock importer.create_fyle_department_payload method
    """
    mock_payload = mocker.patch.object(importer, 'create_fyle_department_payload')
    mock_payload.return_value = [{'name': 'Engineering'}]
    return mock_payload


def mock_send_failure_notification_email(mocker):
    """
    Mock send_failure_notification_email function
    """
    mock_send_email = mocker.patch('fyle_employee_imports.bamboo_hr.send_failure_notification_email')
    return mock_send_email


def mock_send_failure_notification_email_base(mocker):
    """
    Mock send_failure_notification_email function from base module
    """
    mock_send_email = mocker.patch('fyle_employee_imports.base.send_failure_notification_email')
    return mock_send_email


def mock_destination_attribute_bulk_create(mocker):
    """
    Mock DestinationAttribute.bulk_create_or_update_destination_attributes
    """
    mock_bulk_create = mocker.patch('fyle_employee_imports.bamboo_hr.DestinationAttribute.bulk_create_or_update_destination_attributes')
    return mock_bulk_create


def mock_expense_attribute_objects_filter(mocker):
    """
    Mock ExpenseAttribute.objects.filter
    """
    mock_expense_attr = mocker.patch('fyle_employee_imports.base.ExpenseAttribute.objects.filter')
    mock_queryset = MagicMock()
    mock_queryset.exists.return_value = True
    mock_expense_attr.return_value = mock_queryset
    return mock_expense_attr


def mock_destination_attribute_objects_filter(mocker):
    """
    Mock DestinationAttribute.objects.filter
    """
    mock_dest_attr = mocker.patch('fyle_employee_imports.base.DestinationAttribute.objects.filter')
    mock_queryset = MagicMock()
    mock_queryset.exists.return_value = True
    mock_dest_attr.return_value = mock_queryset
    return mock_dest_attr


def mock_importer_methods(mocker, importer):
    """
    Mock common importer methods
    """
    mock_get_employee_payload = mocker.patch.object(importer, 'get_employee_and_approver_payload')
    mock_get_employee_payload.return_value = ([], [])
    
    mock_get_exported_at = mocker.patch.object(importer, 'get_employee_exported_at')
    mock_get_exported_at.return_value = None
    
    mock_save_time = mocker.patch.object(importer, 'save_employee_exported_at_time')
    
    mock_sync_fyle = mocker.patch.object(importer, 'sync_fyle_employees')
    mock_sync_hrms = mocker.patch.object(importer, 'sync_hrms_employees')
    mock_import_dept = mocker.patch.object(importer, 'import_departments')
    mock_fyle_import = mocker.patch.object(importer, 'fyle_employee_import')
    
    return {
        'get_employee_payload': mock_get_employee_payload,
        'get_exported_at': mock_get_exported_at,
        'save_time': mock_save_time,
        'sync_fyle': mock_sync_fyle,
        'sync_hrms': mock_sync_hrms,
        'import_dept': mock_import_dept,
        'fyle_import': mock_fyle_import
    } 
