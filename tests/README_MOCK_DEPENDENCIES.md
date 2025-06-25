# Mock Dependencies Pattern

This document explains how to use the `mock_dependencies` pattern in the Fyle Integrations Settings API test suite. This pattern allows you to use mocks both with the `@pytest.mark.shared_mocks` decorator and as a regular fixture parameter.

## Overview

The `mock_dependencies` pattern provides two ways to work with mocks:

1. **Shared Mocks**: Using `@pytest.mark.shared_mocks` decorator with predefined mock setup functions
2. **Direct Mocks**: Using `mock_dependencies` as a regular fixture parameter and setting up mocks directly in the test

## Pattern 1: Shared Mocks with Decorator

### Step 1: Create Mock Setup Function

Create a function in your `mock_setup.py` file that returns a dictionary of mocks:

```python
# tests/test_bamboohr/mock_setup.py
def mock_bamboohr_shared_mock(mocker):
    """
    Shared mock setup for BambooHR tests
    Returns a dictionary of mocks that can be used with mock_dependencies
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    mock_bamboohr_sdk.employee.get.return_value = {'employees': []}
    
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'bamboohr_sdk': mock_bamboohr_sdk,
        'time_off_get': mock_bamboohr_sdk.time_off.get,
        'employee_get': mock_bamboohr_sdk.employee.get,
    }
```

### Step 2: Use in Test with Decorator

```python
@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_bamboohr_connect_with_shared_mocks(mock_dependencies, api_client, access_token, create_org, db):
    """
    Test bamboohr connect view using shared mocks
    Case: Successfully connects BambooHR with shared mock dependencies
    """
    url = reverse('bamboohr:connect', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    data = {
        'folder_id': 'test_folder',
        'package_id': 'test_package'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    
    # Verify mocks were called correctly
    assert mock_dependencies['bamboohr_sdk'] is not None
    assert mock_dependencies['time_off_get'].call_count >= 0
```

## Pattern 2: Direct Mocks without Decorator

### Using mock_dependencies as Regular Fixture

```python
def test_export_log_sync_view(mock_dependencies, api_client, access_token, create_org, db, mocker):
    """
    Test Export Log Sync View
    Case: Successfully syncs export logs with direct mock setup
    """
    # Set up mocks directly in the test
    mock_queue_import_reimbursable = mocker.patch('apps.integrations.tasks.queue_import_reimbursable_expenses')
    mock_queue_import_credit_card = mocker.patch('apps.integrations.tasks.queue_import_credit_card_expenses')
    
    workspace_id = create_org.id
    url = reverse('integrations:export_logs_sync', kwargs={'workspace_id': workspace_id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    response = api_client.post(url)
    
    assert response.status_code == 200
    assert mock_queue_import_reimbursable.call_count == 1
    assert mock_queue_import_credit_card.call_count == 1
```

### Using mock_dependencies with Custom Setup

```python
def test_bamboohr_employee_import(mock_dependencies, api_client, access_token, create_bamboohr, db, mocker):
    """
    Test bamboohr employee import functionality
    Case: Imports employees using custom mock setup
    """
    # Set up specific mocks for this test
    mock_employee_get = mocker.patch(
        'apps.bamboohr.views.BambooHrSDK.employee.get',
        return_value={'employees': [{'email': 'test@example.com', 'name': 'Test User'}]}
    )
    
    url = reverse('bamboohr:import_employees', kwargs={'org_id': create_bamboohr.org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    
    # Verify the specific mock was called
    assert mock_employee_get.call_count == 1
```

## Available Mock Setup Functions

### BambooHR (`tests/test_bamboohr/mock_setup.py`)
- `mock_bamboohr_shared_mock(mocker)`: Complete BambooHR SDK mock setup

### TravelPerk (`tests/test_travelperk/mock_setup.py`)
- `mock_travelperk_shared_mock(mocker)`: Complete TravelPerk connector mock setup

### Integrations (`tests/test_integrations/mock_setup.py`)
- `mock_integrations_shared_mock(mocker)`: Integration API mock setup

### Orgs (`tests/test_orgs/mock_setup.py`)
- `mock_orgs_shared_mock(mocker)`: Organization and platform mock setup

## Best Practices

### 1. Mock Setup Function Naming
- Use descriptive names that indicate what functionality is being mocked
- Follow the pattern: `mock_{app_name}_shared_mock`

### 2. Return Dictionary Structure
- Return a dictionary with descriptive keys
- Include both the mock objects and their methods for easy access
- Example:
```python
return {
    'bamboohr_sdk': mock_bamboohr_sdk,
    'time_off_get': mock_bamboohr_sdk.time_off.get,
    'employee_get': mock_bamboohr_sdk.employee.get,
}
```

### 3. Test Function Naming
- Use descriptive test names with case numbers
- Follow the pattern: `test_{function_name}_case_{number}`

### 4. Docstrings
- Always include clear docstrings explaining what the test does
- Use "Case:" to describe the specific scenario being tested

### 5. Mock Verification
- Always verify that mocks were called correctly
- Use `assert mock_dependencies['mock_name'].call_count == expected_count`

## Examples by App

### BambooHR Example
```python
@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_bamboohr_connect_case_1(mock_dependencies, api_client, access_token, create_org, db):
    """
    Test bamboohr connect
    Case: Successfully connects with valid credentials
    """
    # Test implementation
    assert mock_dependencies['bamboohr_sdk'] is not None
```

### TravelPerk Example
```python
@pytest.mark.shared_mocks(lambda mocker: mock_travelperk_shared_mock(mocker))
def test_travelperk_connect_case_1(mock_dependencies, api_client, access_token, create_org, db):
    """
    Test travelperk connect
    Case: Successfully creates webhook connection
    """
    # Test implementation
    assert mock_dependencies['create_webhook'].call_count == 1
```

### Integrations Example
```python
@pytest.mark.shared_mocks(lambda mocker: mock_integrations_shared_mock(mocker))
def test_integrations_connect_case_1(mock_dependencies, api_client, access_token, create_org, db):
    """
    Test integrations connect
    Case: Successfully connects integration with valid org
    """
    # Test implementation
    assert mock_dependencies['get_org_id_and_name'].call_count == 1
```

## Migration from Old Pattern

If you have existing tests that use direct `mocker.patch()` calls, you can migrate them to use the `mock_dependencies` pattern:

### Before (Old Pattern)
```python
def test_old_pattern(mocker, api_client):
    mock_sdk = mocker.patch('apps.bamboohr.views.BambooHrSDK')
    # Test implementation
    assert mock_sdk.call_count == 1
```

### After (New Pattern)
```python
@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_new_pattern(mock_dependencies, api_client):
    # Test implementation
    assert mock_dependencies['bamboohr_sdk'] is not None
```

## Troubleshooting

### Common Issues

1. **Mock not found in mock_dependencies**: Make sure the mock setup function returns the mock with the correct key
2. **Shared mocks decorator not working**: Ensure the pytest plugin is properly configured in `conftest.py`
3. **Import errors**: Make sure mock setup functions are properly imported

### Debug Tips

1. Print the mock_dependencies dictionary to see what's available:
```python
def test_debug(mock_dependencies, api_client):
    print("Available mocks:", mock_dependencies.keys())
```

2. Check if mocks are being called:
```python
def test_debug_calls(mock_dependencies, api_client):
    # After making the API call
    print("Mock call count:", mock_dependencies['mock_name'].call_count)
    print("Mock call args:", mock_dependencies['mock_name'].call_args_list)
``` 
