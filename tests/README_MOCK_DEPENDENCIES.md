# Mock Dependencies System

This document explains the comprehensive mock dependency system used in the Fyle Integrations Settings API test suite. The system provides a flexible and maintainable way to handle mocks across different testing scenarios.

## Overview

The mock dependency system consists of three main components:

1. **Session-level mocks** - Global mocks applied to all tests (in `conftest.py`)
2. **Shared mocks** - Reusable mock setups using `@pytest.mark.shared_mocks` decorator
3. **Test-specific mocks** - Individual mocks for specific test cases using naming conventions

## Architecture

### 1. Session-Level Mocks (`conftest.py`)

These are global mocks that apply to all tests and are set up in the `default_session_fixture`:

```python
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
        'apps.users.helpers.get_cluster_domain',
        return_value='https://lolo.fyle.tech'
    )
    patched_2.__enter__()
    
    # ... more session-level mocks
```

**Best Practices:**
- Use for authentication, common external services, and global configurations
- Keep these minimal and focused on cross-cutting concerns
- Don't mock database operations or loggers

### 2. Shared Mocks with Decorator

For complex mock setups that are reused across multiple tests:

#### Step 1: Create Mock Setup Function

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

#### Step 2: Use in Test with Decorator

```python
@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_post_bamboohr_connection_view_case_3(mock_dependencies, api_client, access_token, create_org, db):
    """
    Test post bamboohr connection view
    Case: Valid input returns 200 and creates integration
    """
    url = reverse('bamboohr:connection', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == status.HTTP_200_OK

    # Verify mocks were called correctly
    assert mock_dependencies.bamboohr_sdk is not None
    assert mock_dependencies.time_off_get.call_count >= 0
```

### 3. Test-Specific Mocks

For individual test cases, use the naming convention `mock_{test_function_name}`:

#### Step 1: Create Test-Specific Mock Function

```python
# tests/test_users/mock_setup.py
def mock_test_get_cluster_domain_case_1(mocker):
    """
    Mock setup for test_get_cluster_domain_case_1
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"cluster_domain": "https://test.fyle.tech"}'
    
    mock_post = mocker.patch('apps.users.helpers.requests.post', return_value=mock_response)
    return mock_post
```

#### Step 2: Use in Test (Automatic Loading)

```python
def test_get_cluster_domain_case_1(mock_dependencies, api_client, mocker, access_token, db):
    """
    Test get_cluster_domain helper
    Case: Returns correct cluster domain
    """
    cluster_domain = get_cluster_domain('dummy_access_token')
    assert cluster_domain == 'https://lolo.fyle.tech'  # Uses session-level mock
```

## Mock Setup File Structure

Each app should have its own `mock_setup.py` file:

```
tests/
├── test_bamboohr/
│   ├── mock_setup.py          # BambooHR-specific mocks
│   ├── test_views.py
│   └── fixtures.py
├── test_travelperk/
│   ├── mock_setup.py          # TravelPerk-specific mocks
│   ├── test_views.py
│   └── fixtures.py
├── test_integrations/
│   ├── mock_setup.py          # Integration-specific mocks
│   ├── test_views.py
│   └── fixture.py
└── conftest.py                # Global fixtures and session mocks
```

## Available Mock Setup Functions

### BambooHR (`tests/test_bamboohr/mock_setup.py`)
- `mock_bamboohr_shared_mock(mocker)`: Complete BambooHR SDK mock setup
- `mock_bamboohr_invalid_token_shared_mock(mocker)`: Invalid token scenario
- `mock_bamboohr_sdk_valid_token(mocker)`: Valid token response
- `mock_bamboohr_sdk_invalid_token(mocker)`: Invalid token response

### TravelPerk (`tests/test_travelperk/mock_setup.py`)
- `mock_travelperk_shared_mock(mocker)`: Complete TravelPerk connector mock setup
- `mock_travelperk_webhook_creation(mocker)`: Webhook creation scenarios
- `mock_travelperk_invoice_processing(mocker)`: Invoice processing mocks

### Integrations (`tests/test_integrations/mock_setup.py`)
- `mock_integrations_shared_mock(mocker)`: Integration API mock setup
- `mock_queue_import_tasks(mocker)`: Queue import task mocks

### Users (`tests/test_users/mock_setup.py`)
- `mock_test_get_cluster_domain_case_1(mocker)`: Cluster domain retrieval
- `mock_test_post_request_case_1(mocker)`: HTTP POST request success
- `mock_test_post_request_case_2(mocker)`: HTTP POST request failure

## Best Practices

### 1. Mock Setup Function Naming

**Shared Mocks:**
```python
def mock_{app_name}_shared_mock(mocker):
    """Shared mock setup for {AppName} tests"""
```

**Test-Specific Mocks:**
```python
def mock_{test_function_name}(mocker):
    """Mock setup for {test_function_name}"""
```

### 2. Return Structure

**Shared Mocks:** Return a dictionary with descriptive keys
```python
return {
    'bamboohr_sdk': mock_bamboohr_sdk,
    'time_off_get': mock_bamboohr_sdk.time_off.get,
    'employee_get': mock_bamboohr_sdk.employee.get,
}
```

**Test-Specific Mocks:** Return the mock object directly
```python
return mock_post
```

### 3. Test Function Naming Convention

```python
def test_{function_name}_case_{number}(mock_dependencies, ...):
    """
    Test {function_name}
    Case: {specific scenario description}
    """
```

### 4. Mock Verification

Always verify that mocks were called correctly:

```python
# For shared mocks
assert mock_dependencies.bamboohr_sdk is not None
assert mock_dependencies.time_off_get.call_count == 1

# For test-specific mocks
assert mock_dependencies.call_count == 1
assert mock_dependencies.call_args == expected_args
```

### 5. Docstrings

Every test function must have a clear docstring:

```python
def test_function_name(mock_dependencies, ...):
    """
    Test function_name
    Case: Specific scenario being tested
    """
```

## Examples by App

### BambooHR Example

```python
@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_post_bamboohr_connection_view_case_3(mock_dependencies, api_client, access_token, create_org, db):
    """
    Test post bamboohr connection view
    Case: Valid input returns 200 and creates integration
    """
    url = reverse('bamboohr:connection', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, fixture['bamboo_connection'], format='json')
    assert response.status_code == status.HTTP_200_OK

    # Verify integration was created
    integration_object = Integration.objects.get(org_id=create_org.fyle_org_id, type='HRMS')
    assert integration_object is not None
    assert integration_object.is_active is True
```

### TravelPerk Example

```python
@pytest.mark.shared_mocks(lambda mocker: mock_travelperk_shared_mock(mocker))
def test_connect_travelperk_case_1(mock_dependencies, api_client, access_token, create_org, db):
    """
    Test connect travelperk
    Case: Successfully creates webhook connection
    """
    url = reverse('travelperk:connect', kwargs={'org_id': create_org.id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.post(url, fixture['travelperk_connection'], format='json')
    assert response.status_code == status.HTTP_200_OK

    # Verify webhook was created
    assert mock_dependencies.create_webhook.call_count == 1
```

### Integrations Example

```python
def test_export_log_sync_view(mock_dependencies, api_client, access_token, create_org, db):
    """
    Test Export Log Sync View
    Case: Successfully syncs export logs
    """
    workspace_id = create_org.id
    url = reverse('integrations:export_logs_sync', kwargs={'workspace_id': workspace_id})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    response = api_client.post(url)
    
    assert response.status_code == 200
    assert mock_dependencies.queue_import_reimbursable_expenses.call_count == 1
    assert mock_dependencies.queue_import_credit_card_expenses.call_count == 1
```

## Migration Guide

### From Direct Mocker Usage

**Before:**
```python
def test_old_pattern(mocker, api_client):
    mock_sdk = mocker.patch('apps.bamboohr.views.BambooHrSDK')
    # Test implementation
    assert mock_sdk.call_count == 1
```

**After:**
```python
@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_new_pattern(mock_dependencies, api_client):
    # Test implementation
    assert mock_dependencies.bamboohr_sdk is not None
```

### From Inline Mock Setup

**Before:**
```python
def test_inline_mocks(mocker, api_client):
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mocker.patch('requests.post', return_value=mock_response)
    # Test implementation
```

**After:**
```python
def test_structured_mocks(mock_dependencies, api_client):
    # Mock is automatically loaded from mock_setup.py
    # Test implementation
```

## Troubleshooting

### Common Issues

1. **Mock not found in mock_dependencies**
   - Ensure the mock setup function returns the mock with the correct key
   - Check that the shared mocks decorator is properly applied

2. **Test-specific mock function not found**
   - Verify the function name follows the convention: `mock_{test_function_name}`
   - Check that the function is in the correct `mock_setup.py` file

3. **Session-level mocks overriding test mocks**
   - Session-level mocks are applied first and may override test-specific mocks
   - Use test-specific mocks for scenarios that need different behavior

### Debug Tips

1. **Print available mocks:**
```python
def test_debug(mock_dependencies, api_client):
    print("Available mocks:", dir(mock_dependencies))
```

2. **Check mock call details:**
```python
def test_debug_calls(mock_dependencies, api_client):
    # After making the API call
    print("Mock call count:", mock_dependencies.mock_name.call_count)
    print("Mock call args:", mock_dependencies.mock_name.call_args_list)
```

3. **Verify mock setup loading:**
```python
def test_verify_mock_loading(mock_dependencies, api_client):
    # Check if specific mock is available
    assert hasattr(mock_dependencies, 'expected_mock_name')
```

## Critical Rules

1. **Never mock database operations** - Use real database transactions with `db` argument
2. **Never mock loggers** - Let them work normally
3. **Always mock external services** - API calls, HTTP requests, external SDKs
4. **Use fixtures for test data** - Never create objects inline in tests
5. **Follow naming conventions** - Test functions and mock functions must follow established patterns
6. **Verify mock calls** - Always assert that mocks were called correctly
7. **Use descriptive docstrings** - Every test must have a clear docstring with "Case:" description 
