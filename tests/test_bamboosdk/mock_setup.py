from .fixtures import (
    employee_list_response,
    single_employee_response,
    time_off_types_response,
    mock_response_200,
    mock_response_201,
    mock_response_401,
    mock_response_403,
    mock_response_404,
    mock_response_500,
    status_200,
    status_201,
    status_401,
    status_403,
    status_404,
    status_500,
    error_401_message,
    error_403_message,
    error_404_message,
    error_500_message
)


def mock_requests_get_success(mocker):
    """Mock successful GET request"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_200
    mock_response.text = '{"success": true, "data": "test_data"}'
    return mocker.patch('requests.get', return_value=mock_response)


def mock_requests_post_success(mocker):
    """Mock successful POST request"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_201
    mock_response.text = '{"success": true, "data": "created"}'
    return mocker.patch('requests.post', return_value=mock_response)


def mock_requests_delete_success(mocker):
    """Mock successful DELETE request"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_200
    mock_response.text = '{"message": "Webhook has been deleted"}'
    return mocker.patch('requests.delete', return_value=mock_response)


def mock_requests_get_401_error(mocker):
    """Mock GET request with 401 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_401
    mock_response.text = error_401_message
    return mocker.patch('requests.get', return_value=mock_response)


def mock_requests_get_403_error(mocker):
    """Mock GET request with 403 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_403
    mock_response.text = error_403_message
    return mocker.patch('requests.get', return_value=mock_response)


def mock_requests_get_404_error(mocker):
    """Mock GET request with 404 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_404
    mock_response.text = error_404_message
    return mocker.patch('requests.get', return_value=mock_response)


def mock_requests_get_500_error(mocker):
    """Mock GET request with 500 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_500
    mock_response.text = error_500_message
    return mocker.patch('requests.get', return_value=mock_response)


def mock_requests_post_401_error(mocker):
    """Mock POST request with 401 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_401
    mock_response.text = error_401_message
    return mocker.patch('requests.post', return_value=mock_response)


def mock_requests_post_403_error(mocker):
    """Mock POST request with 403 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_403
    mock_response.text = error_403_message
    return mocker.patch('requests.post', return_value=mock_response)


def mock_requests_post_404_error(mocker):
    """Mock POST request with 404 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_404
    mock_response.text = error_404_message
    return mocker.patch('requests.post', return_value=mock_response)


def mock_requests_post_500_error(mocker):
    """Mock POST request with 500 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_500
    mock_response.text = error_500_message
    return mocker.patch('requests.post', return_value=mock_response)


def mock_requests_delete_401_error(mocker):
    """Mock DELETE request with 401 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_401
    mock_response.text = error_401_message
    return mocker.patch('requests.delete', return_value=mock_response)


def mock_requests_delete_403_error(mocker):
    """Mock DELETE request with 403 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_403
    mock_response.text = error_403_message
    return mocker.patch('requests.delete', return_value=mock_response)


def mock_requests_delete_404_error(mocker):
    """Mock DELETE request with 404 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_404
    mock_response.text = error_404_message
    return mocker.patch('requests.delete', return_value=mock_response)


def mock_requests_delete_500_error(mocker):
    """Mock DELETE request with 500 error"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_500
    mock_response.text = error_500_message
    return mocker.patch('requests.delete', return_value=mock_response)


def mock_employees_get_all_success(mocker):
    """Mock successful Employee.get_all() response"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_200
    mock_response.text = str(employee_list_response).replace("'", '"')
    return mocker.patch('requests.post', return_value=mock_response)


def mock_employees_get_success(mocker):
    """Mock successful Employee.get() response"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_200
    mock_response.text = str(single_employee_response).replace("'", '"')
    return mocker.patch('requests.get', return_value=mock_response)


def mock_time_off_get_success(mocker):
    """Mock successful TimeOff.get() response"""
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_200
    mock_response.text = str(time_off_types_response).replace("'", '"')
    return mocker.patch('requests.get', return_value=mock_response)


def mock_base64_encode(mocker):
    """Mock base64 encoding"""
    return mocker.patch('base64.b64encode', return_value=b'dGVzdF9hcGlfdG9rZW46YQ==')


def mock_json_loads(mocker):
    """Mock JSON loads for successful responses"""
    return mocker.patch('json.loads', return_value={'success': True, 'data': 'test_data'})


def mock_test_employee_get_all_without_incremental_sync(mocker):
    """Mock for test_employee_get_all_without_incremental_sync"""
    return mock_employees_get_all_success(mocker)


def mock_test_employee_get_all_with_incremental_sync(mocker):
    """Mock for test_employee_get_all_with_incremental_sync"""
    return mock_employees_get_all_success(mocker)


def mock_test_employee_get_all_with_incremental_sync_none_date(mocker):
    """Mock for test_employee_get_all_with_incremental_sync_none_date"""
    return mock_employees_get_all_success(mocker)


def mock_test_employee_get_all_401_error(mocker):
    """Mock for test_employee_get_all_401_error"""
    return mock_requests_post_401_error(mocker)


def mock_test_employee_get_all_403_error(mocker):
    """Mock for test_employee_get_all_403_error"""
    return mock_requests_post_403_error(mocker)


def mock_test_employee_get_all_404_error(mocker):
    """Mock for test_employee_get_all_404_error"""
    return mock_requests_post_404_error(mocker)


def mock_test_employee_get_all_500_error(mocker):
    """Mock for test_employee_get_all_500_error"""
    return mock_requests_post_500_error(mocker)


def mock_test_employee_get_success(mocker):
    """Mock for test_employee_get_success"""
    return mock_employees_get_success(mocker)


def mock_test_employee_get_401_error(mocker):
    """Mock for test_employee_get_401_error"""
    return mock_requests_get_401_error(mocker)


def mock_test_employee_get_403_error(mocker):
    """Mock for test_employee_get_403_error"""
    return mock_requests_get_403_error(mocker)


def mock_test_employee_get_404_error(mocker):
    """Mock for test_employee_get_404_error"""
    return mock_requests_get_404_error(mocker)


def mock_test_employee_get_500_error(mocker):
    """Mock for test_employee_get_500_error"""
    return mock_requests_get_500_error(mocker)


def mock_test_employee_payload_modification(mocker):
    """Mock for test_employee_payload_modification"""
    return mock_employees_get_all_success(mocker)


def mock_test_employee_with_none_values(mocker):
    """Mock for test_employee_with_none_values"""
    return mock_employees_get_success(mocker)


def mock_test_employee_with_empty_string_id(mocker):
    """Mock for test_employee_with_empty_string_id"""
    return mock_employees_get_success(mocker) 
