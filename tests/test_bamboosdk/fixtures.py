api_token = 'test_api_token'
sub_domain = 'test_subdomain'
invalid_api_token = 'invalid_token'
invalid_sub_domain = 'invalid_subdomain'

employee_id = '123'

employee_report_payload = {
    'fields': ['displayName', 'firstName', 'lastName', 'department', 'workEmail', 'supervisorEmail', 'status']
}

employee_report_incremental_payload = {
    'fields': ['displayName', 'firstName', 'lastName', 'department', 'workEmail', 'supervisorEmail', 'status'],
    'filters': {
        'lastChanged': {
            'includeNull': 'yes',
            'value': '2024-01-01T00:00:00+00:00'
        }
    }
}

employee_list_response = {
    'employees': [
        {
            'id': '123',
            'displayName': 'John Doe',
            'firstName': 'John',
            'lastName': 'Doe',
            'department': 'Engineering',
            'workEmail': 'john.doe@example.com',
            'supervisorEmail': 'supervisor@example.com',
            'status': 'Active'
        },
        {
            'id': '456',
            'displayName': 'Jane Smith',
            'firstName': 'Jane',
            'lastName': 'Smith',
            'department': 'Marketing',
            'workEmail': 'jane.smith@example.com',
            'supervisorEmail': 'manager@example.com',
            'status': 'Active'
        }
    ]
}

single_employee_response = {
    'id': '123',
    'workEmail': 'john.doe@example.com'
}

time_off_types_response = {
    'timeOffTypes': [
        {
            'id': '1',
            'name': 'Vacation',
            'units': 'days',
            'color': '#FF0000'
        },
        {
            'id': '2',
            'name': 'Sick Leave',
            'units': 'days',
            'color': '#00FF00'
        }
    ]
}

sync_employee_from_date = '2024-01-01T00:00:00+00:00'

# HTTP Status Codes
status_200 = 200
status_201 = 201
status_401 = 401
status_403 = 403
status_404 = 404
status_500 = 500

# Error Messages
error_401_message = 'Unauthorized access'
error_403_message = 'Forbidden access'
error_404_message = 'Resource not found'
error_500_message = 'Internal server error'

# API URLs
employee_report_url = '/v1/reports/custom?format=JSON&onlyCurrent=false'
employee_by_id_url = '/v1/employees/123/?fields=workEmail&onlyCurrent=false'
time_off_types_url = '/v1/meta/time_off/types/'

# Test credentials
base64_credentials = 'testing_credentials_string'

# Headers
expected_headers = {
    'Accept': 'application/json',
    'content-type': 'application/json',
    'authorization': f'Basic {base64_credentials}'
}

# Request response mock data
mock_response_200 = {
    'status_code': 200,
    'text': '{"success": true, "data": "test_data"}'
}

mock_response_201 = {
    'status_code': 201,
    'text': '{"success": true, "data": "created"}'
}

mock_response_401 = {
    'status_code': 401,
    'text': error_401_message
}

mock_response_403 = {
    'status_code': 403,
    'text': error_403_message
}

mock_response_404 = {
    'status_code': 404,
    'text': error_404_message
}

mock_response_500 = {
    'status_code': 500,
    'text': error_500_message
} 
