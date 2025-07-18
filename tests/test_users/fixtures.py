# Static test data for mocks
cluster_domain_response = '{"cluster_domain": "https://test.fyle.tech"}'
bad_request_response = 'Bad Request'

# PlatformConnector test data
dummy_refresh_token = 'dummy_refresh_token'
test_cluster_domain = 'https://test.fyle.tech'
test_email = 'test@example.com'
test_org_id = 1

# Post request headers
post_request_headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer dummy_access_token'
}

# Employee test data
test_employee_bulk_payload = [{'user_email': 'test@example.com'}]

# Department test data
test_department_data = {'name': 'Test Dept'}
test_department_query_params = {'order': 'id.desc'}

# Mock API responses
empty_employee_response = {'data': []}
empty_department_response = {'data': []}

# Mock employee data for sync_employees (to trigger line 65)
mock_employee_sync_response = [{
    'data': [{
        'id': 'emp123',
        'user_id': 'user123',
        'code': 'E001',
        'user': {'email': 'test@example.com', 'full_name': 'Test User'},
        'location': 'Test Location',
        'department': {'name': 'Engineering', 'code': 'ENG'},
        'department_id': 'dept123'
    }]
}]

# Mock category data for sync_categories (to trigger lines 95-98)
mock_category_sync_response = [{
    'data': [{
        'id': 'cat123',
        'name': 'Travel',
        'sub_category': 'Flight',
        'is_enabled': True
    }]
}]

# Expected API call parameters
employee_list_query_params = {
    'user->email': 'eq.test@example.com',
    'offset': 0,
    'limit': 1,
    'order': 'updated_at.desc'
}

# Employee data for simple tests
employee_list_query_params = {
    'user->email': 'eq.test@example.com',
    'offset': 0,
    'limit': 1,
    'order': 'updated_at.desc'
}

employees_bulk_invite_payload = {
    'data': [
        {
            'user_email': 'employee1@example.com',
            'user_full_name': 'Employee One'
        },
        {
            'user_email': 'employee2@example.com',
            'user_full_name': 'Employee Two'
        }
    ]
}

# Department data for simple tests
department_list_query_params = {
    'order': 'id.desc'
}

department_post_payload = {
    'data': {
        'name': 'New Department',
        'code': 'NEW'
    }
}

# Category data for simple tests
category_list_query_params = {
    'is_enabled': 'eq.true',
    'order': 'updated_at.desc'
}

# Employee sync data for simple tests
employee_sync_query_params = {
    'is_enabled': 'eq.true',
    'order': 'updated_at.desc'
} 
