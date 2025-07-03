from datetime import datetime, timezone

dummy_org_id = 1
dummy_refresh_token = 'dummy_refresh_token'
cluster_domain = 'https://test.fyle.tech'

# Employee data for testing
employee_data = [
    {
        'id': '123',
        'firstName': 'John',
        'lastName': 'Doe',
        'workEmail': 'john.doe@example.com',
        'status': 'Active',
        'department': 'Engineering',
        'supervisorEmail': 'supervisor@example.com',
        'displayName': 'John Doe'
    },
    {
        'id': '456',
        'firstName': 'Jane',
        'lastName': 'Smith',
        'workEmail': 'jane.smith@example.com',
        'status': 'Active',
        'department': 'Marketing',
        'supervisorEmail': None,
        'displayName': 'Jane Smith'
    }
]

# Employee data without email
employee_data_no_email = [
    {
        'id': '789',
        'firstName': 'Bob',
        'lastName': 'Johnson',
        'workEmail': None,
        'status': 'Active',
        'department': 'Sales',
        'supervisorEmail': None,
        'displayName': 'Bob Johnson'
    }
]

# BambooHR employees response format
bamboohr_employees_response = {
    'employees': employee_data + employee_data_no_email
}

# Existing departments from Fyle
existing_departments_response = {
    'Engineering': {
        'id': 'dept_123',
        'is_enabled': True
    },
    'Marketing': {
        'id': 'dept_456',
        'is_enabled': False
    }
}

# Department generator response
department_generator_response = [
    {
        'id': 'dept_123',
        'name': 'Engineering',
        'display_name': 'Engineering',
        'is_enabled': True
    },
    {
        'id': 'dept_456',
        'name': 'Marketing',
        'display_name': 'Marketing',
        'is_enabled': False
    }
]

# New departments to be imported
new_departments = ['Sales', 'HR']

# Department payload
department_payload = [
    {
        'name': 'Sales',
        'display_name': 'Sales'
    },
    {
        'name': 'HR',
        'display_name': 'HR'
    }
]

# Employee payload
employee_payload = [
    {
        'user_email': 'john.doe@example.com',
        'user_full_name': 'John Doe',
        'code': '123',
        'department_name': 'Engineering',
        'is_enabled': True
    }
]

# Employee approver payload
employee_approver_payload = [
    {
        'user_email': 'john.doe@example.com',
        'approver_emails': ['supervisor@example.com']
    }
]

# Incomplete employees
incomplete_employees = [
    {
        'name': 'Bob Johnson',
        'id': '789'
    }
]

# BambooHR configuration data
bamboohr_config_data = {
    'emails_selected': [
        {'name': 'Admin', 'email': 'admin@example.com'},
        {'name': 'Manager', 'email': 'manager@example.com'}
    ]
}

# Admin emails
admin_emails = ['admin@example.com', 'manager@example.com']

# Webhook payload
webhook_payload = {
    'firstName': 'John',
    'lastName': 'Doe',
    'workEmail': 'john.doe@example.com',
    'status': True,
    'department': 'Engineering',
    'supervisorEId': '999',
    'id': '123'
}

# Webhook payload without email
webhook_payload_no_email = {
    'firstName': 'Bob',
    'lastName': 'Johnson',
    'workEmail': None,
    'status': True,
    'department': 'Sales',
    'supervisorEId': None,
    'id': '789'
}

# Supervisor employee data
supervisor_employee_data = {
    'workEmail': 'supervisor@example.com',
    'firstName': 'Super',
    'lastName': 'Visor',
    'status': 'Active'
}

# Fyle employee response
fyle_employee_response = [
    {
        'id': 'emp_123',
        'user_email': 'supervisor@example.com',
        'user_full_name': 'Super Visor'
    }
]

# BambooHR incremental sync data
sync_employee_from_date = '2024-01-01T00:00:00'

# Destination attributes for testing
destination_attributes = [
    {
        'detail': {
            'email': 'john.doe@example.com',
            'full_name': 'John Doe',
            'department_name': 'Engineering',
            'approver_emails': ['supervisor@example.com']
        },
        'destination_id': '123',
        'active': True
    }
]

# Employee exported at time
employee_exported_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

# Email notification data
email_notification_employees = [
    {
        'detail__full_name': 'Bob Johnson',
        'destination_id': '789'
    }
]

# Expense attributes for approver emails
expense_attributes = [
    ('john.doe@example.com', 'category_1'),
    ('jane.smith@example.com', 'category_2'),
    ('supervisor@example.com', 'category_3')
]

# Department creation payload
department_creation_payload = {
    'name': 'Engineering',
    'display_name': 'Engineering',
    'is_enabled': True
}

# BambooHR data for fixtures
bamboohr_data = {
    'api_token': 'test_token',
    'sub_domain': 'test_domain',
    'employee_exported_at': employee_exported_at
}

# BambooHR configuration data for fixtures
bamboohr_configuration_data = {
    'emails_selected': [
        {'name': 'Admin', 'email': 'admin@example.com'},
        {'name': 'Manager', 'email': 'manager@example.com'}
    ]
}

# Fyle credential data
fyle_credential_data = {
    'refresh_token': dummy_refresh_token,
    'cluster_domain': cluster_domain
}

# Query parameters for department generator
department_query_params = {
    'order': 'id.desc'
}

# Employee list query parameters
employee_list_query_params = {
    'user->email': 'eq.supervisor@example.com',
    'offset': 0,
    'limit': 1,
    'order': 'updated_at.desc'
}

# BambooHR SDK employees response
bamboohr_sdk_employees_response = {
    'employees': employee_data
}

# Incremental sync parameters
incremental_sync_params = {
    'is_incremental_sync': True,
    'sync_employee_from': sync_employee_from_date
}

# Non-incremental sync parameters
non_incremental_sync_params = {
    'is_incremental_sync': False,
    'sync_employee_from': None
}

org_created_at = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

# Test mock employees for departments_to_be_imported
mock_employees_for_departments = [
    {
        'detail': {'department_name': 'Engineering'},
    },
    {
        'detail': {'department_name': 'Marketing'},
    },
    {
        'detail': {'department_name': 'Engineering'},
    },
    {
        'detail': {'department_name': None},
    }
]

# Expected department set result
expected_departments_set = ['Marketing', 'Engineering']

# Test mock employees for import_departments
mock_employees_for_import = [
    {
        'detail': {'department_name': 'Sales'},
    },
    {
        'detail': {'department_name': 'HR'},
    }
]

# Expected department payload
expected_department_payload = [
    {
        'name': 'Sales',
        'display_name': 'Sales'
    },
    {
        'name': 'HR',
        'display_name': 'HR'
    }
]

# Expected disabled department payload
expected_disabled_department_payload = [
    {
        'name': 'Marketing',
        'id': 'dept_456',
        'is_enabled': True,
        'display_name': 'Marketing'
    }
]

# Mock employees for get_employee_and_approver_payload
mock_employees_for_payload = [
    {
        'detail': {
            'email': 'john.doe@example.com',
            'full_name': 'John Doe',
            'department_name': 'Engineering',
            'approver_emails': ['supervisor@example.com']
        },
        'destination_id': '123',
        'active': True
    },
    {
        'detail': {
            'email': None,
            'full_name': 'Bob Johnson',
            'department_name': 'Sales',
            'approver_emails': []
        },
        'destination_id': '789',
        'active': True
    }
]

# Expected employee payload result
expected_employee_payload_result = [
    {
        'user_email': 'john.doe@example.com',
        'user_full_name': 'John Doe',
        'code': '123',
        'department_name': 'Engineering',
        'is_enabled': True
    }
]

# Expected approver payload result
expected_approver_payload_result = [
    {
        'user_email': 'john.doe@example.com',
        'approver_emails': ['supervisor@example.com']
    }
]

# Mock employees for fyle_employee_import
mock_employees_for_import_process = [
    {
        'detail': {
            'email': 'john.doe@example.com',
            'full_name': 'John Doe',
            'department_name': 'Engineering',
            'approver_emails': ['supervisor@example.com']
        },
        'destination_id': '123',
        'active': True
    },
    {
        'detail': {
            'email': 'jane.smith@example.com',
            'full_name': 'Jane Smith',
            'department_name': 'Marketing',
            'approver_emails': []
        },
        'destination_id': '456',
        'active': True
    }
]

# Inactive employee response for testing
inactive_employee_response = {
    'employees': [
        {
            'id': '999',
            'firstName': 'Inactive',
            'lastName': 'Employee',
            'displayName': 'Inactive Employee',
            'workEmail': 'inactive@example.com',
            'department': 'HR',
            'supervisorEmail': None,
            'status': 'Inactive'
        }
    ]
}

# Webhook payload without supervisor
webhook_payload_no_supervisor = {
    'firstName': 'Jane',
    'lastName': 'Smith',
    'workEmail': 'jane.smith@example.com',
    'status': True,
    'department': 'Marketing',
    'supervisorEId': None,
    'id': '456'
}

# Webhook payload with new department
webhook_payload_with_dept = {
    'firstName': 'John',
    'lastName': 'Doe',
    'workEmail': 'john.doe@example.com',
    'status': True,
    'department': 'New Department',
    'supervisorEId': None,
    'id': '123'
}

# Employee with missing display name
employee_missing_display_name = {
    'employees': [
        {
            'id': '555',
            'firstName': 'Missing',
            'lastName': 'DisplayName',
            'workEmail': 'missing@example.com',
            'status': 'Active',
            'department': 'IT',
            'supervisorEmail': None,
            'displayName': None
        }
    ]
}

# Expected DestinationAttribute data for database operations
expected_destination_attributes_data = [
    {
        'attribute_type': 'EMPLOYEE',
        'value': 'John Doe',
        'destination_id': '123',
        'detail': {
            'email': 'john.doe@example.com',
            'department_name': 'Engineering',
            'full_name': 'John Doe',
            'approver_emails': ['supervisor@example.com']
        },
        'active': True
    },
    {
        'attribute_type': 'EMPLOYEE',
        'value': 'Jane Smith',
        'destination_id': '456',
        'detail': {
            'email': 'jane.smith@example.com',
            'department_name': 'Marketing',
            'full_name': 'Jane Smith',
            'approver_emails': [None]
        },
        'active': True
    },
    {
        'attribute_type': 'EMPLOYEE',
        'value': 'Bob Johnson',
        'destination_id': '789',
        'detail': {
            'email': None,
            'department_name': 'Sales',
            'full_name': 'Bob Johnson',
            'approver_emails': [None]
        },
        'active': True
    }
]

# Expected inactive employee DestinationAttribute data
expected_inactive_employee_data = [
    {
        'attribute_type': 'EMPLOYEE',
        'value': 'Inactive Employee',
        'destination_id': '999',
        'detail': {
            'email': 'inactive@example.com',
            'department_name': 'HR',
            'full_name': 'Inactive Employee',
            'approver_emails': [None]
        },
        'active': False
    }
]
