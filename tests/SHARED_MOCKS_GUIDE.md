# Shared Mocks Guide for Settings-API

This guide explains how to use shared mocks in the settings-api project, following the patterns from the connector-api.

## Overview

Shared mocks allow you to define reusable mock configurations that can be applied to multiple tests. This reduces code duplication and ensures consistent mocking across your test suite.

## Infrastructure

### 1. Conftest.py Setup

The shared mocks infrastructure is already set up in `tests/conftest.py`:

```python
@pytest.fixture(autouse=True)
def shared_mocks(request, mocker):
    """
    Apply shared mocks to tests marked with @pytest.mark.shared_mocks
    """
    shared_mocks_marker = request.node.get_closest_marker("shared_mocks")
    if shared_mocks_marker:
        for mock_func in shared_mocks_marker.args:
            shared_mocks = mock_func(mocker)
            for key, value in shared_mocks.items():
                setattr(request.function, key, value)
```

### 2. Mock Setup Files

Create `mock_setup.py` files in each test directory to define shared mock functions:

```
tests/
├── test_bamboohr/
│   ├── mock_setup.py
│   └── test_views.py
├── test_integrations/
│   ├── mock_setup.py
│   └── test_views.py
└── test_orgs/
    ├── mock_setup.py
    └── test_views.py
```

## Creating Shared Mock Functions

### Basic Structure

```python
# tests/test_app/mock_setup.py
from unittest.mock import MagicMock

def mock_success_scenario_shared_mock(mocker):
    """
    Shared mock for success scenarios
    """
    # Create mocks
    mock_external_api = mocker.patch('apps.app.actions.external_api')
    mock_external_api.return_value = {'status': 'success'}
    
    # Return dictionary of mocks for test access
    return {
        'mock_external_api': mock_external_api
    }
```

### Advanced Example

```python
def mock_complex_operation_shared_mock(mocker):
    """
    Shared mock for complex operations with multiple dependencies
    """
    # Mock external services
    mock_api_client = mocker.patch('apps.app.actions.APIClient')
    mock_api_instance = MagicMock()
    mock_api_client.return_value = mock_api_instance
    mock_api_instance.get.return_value = {'data': 'success'}
    
    # Mock database operations
    mock_db_operation = mocker.patch('apps.app.actions.database_operation')
    mock_db_operation.return_value = True
    
    # Mock email sending
    mock_send_email = mocker.patch('apps.app.actions.send_email')
    
    return {
        'mock_api_client': mock_api_client,
        'mock_api_instance': mock_api_instance,
        'mock_db_operation': mock_db_operation,
        'mock_send_email': mock_send_email
    }
```

## Using Shared Mocks in Tests

### Basic Usage

```python
@pytest.mark.shared_mocks(lambda mocker: mock_success_scenario_shared_mock(mocker))
@pytest.mark.django_db(databases=['default'])
def test_success_scenario(api_client, access_token, mock_external_api):
    """
    Test using shared mocks
    """
    # Your test logic here
    response = api_client.get('/api/endpoint')
    assert response.status_code == 200
    
    # Verify mocks were called
    mock_external_api.assert_called_once()
```

### Multiple Shared Mocks

```python
@pytest.mark.shared_mocks(
    lambda mocker: mock_success_scenario_shared_mock(mocker),
    lambda mocker: mock_another_scenario_shared_mock(mocker)
)
@pytest.mark.django_db(databases=['default'])
def test_with_multiple_mocks(api_client, access_token, mock_external_api, mock_another_service):
    """
    Test using multiple shared mocks
    """
    # Test logic
    pass
```

### Combining Shared Mocks

```python
@pytest.mark.shared_mocks(
    lambda mocker: {**mock_success_scenario_shared_mock(mocker), **mock_another_scenario_shared_mock(mocker)}
)
@pytest.mark.django_db(databases=['default'])
def test_with_combined_mocks(api_client, access_token, mock_external_api, mock_another_service):
    """
    Test using combined shared mocks
    """
    # Test logic
    pass
```

## Real-World Examples

### BambooHR SDK Mocks

```python
# tests/test_bamboohr/mock_setup.py
def mock_bamboohr_sdk_success_shared_mock(mocker):
    """
    Shared mock for successful BambooHR SDK operations
    """
    mock_bamboohr_sdk = MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    mock_bamboohr_sdk.employees.get.return_value = {'employees': []}
    
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    mocker.patch('apps.bamboohr.actions.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'mock_bamboohr_sdk': mock_bamboohr_sdk
    }
```

### Usage in Tests

```python
@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_sdk_success_shared_mock(mocker))
@pytest.mark.django_db(databases=['default'])
def test_bamboohr_health_check(api_client, access_token, get_org_id, mock_bamboohr_sdk):
    """
    Test BambooHR health check using shared mocks
    """
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))
    
    url = reverse('bamboohr:health-check', kwargs={'org_id': get_org_id})
    response = api_client.get(url)
    assert response.status_code == 200
    
    # Verify mock was called
    mock_bamboohr_sdk.time_off.get.assert_called_once()
```

## Best Practices

### 1. Naming Conventions

- Use descriptive names: `mock_success_scenario_shared_mock`
- Include the scenario in the name: `mock_invalid_token_shared_mock`
- Use consistent naming patterns across apps

### 2. Mock Organization

- Group related mocks in the same function
- Return a dictionary with descriptive keys
- Document what each mock does

### 3. Reusability

- Create mocks that can be used across multiple test scenarios
- Avoid overly specific mocks that are only used once
- Consider parameterizing mocks for different scenarios

### 4. Verification

- Always verify that mocks were called correctly
- Use appropriate assertion methods (`assert_called_once`, `assert_called_with`, etc.)
- Test both success and failure scenarios

### 5. Error Scenarios

```python
def mock_error_scenario_shared_mock(mocker):
    """
    Shared mock for error scenarios
    """
    mock_external_api = mocker.patch('apps.app.actions.external_api')
    mock_external_api.side_effect = Exception('API Error')
    
    return {
        'mock_external_api': mock_external_api
    }
```

## Common Patterns

### 1. External API Mocks

```python
def mock_external_api_shared_mock(mocker):
    """
    Mock external API calls
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': 'success'}
    
    mock_requests = mocker.patch('apps.app.actions.requests.get')
    mock_requests.return_value = mock_response
    
    return {
        'mock_requests': mock_requests,
        'mock_response': mock_response
    }
```

### 2. Database Operation Mocks

```python
def mock_database_operation_shared_mock(mocker):
    """
    Mock database operations
    """
    mock_query = mocker.patch('apps.app.models.Model.objects.filter')
    mock_query.return_value.exists.return_value = True
    
    return {
        'mock_query': mock_query
    }
```

### 3. Email Service Mocks

```python
def mock_email_service_shared_mock(mocker):
    """
    Mock email services
    """
    mock_sendgrid = mocker.patch('apps.app.actions.SendGridAPIClient')
    mock_sendgrid_instance = MagicMock()
    mock_sendgrid.return_value = mock_sendgrid_instance
    
    return {
        'mock_sendgrid': mock_sendgrid,
        'mock_sendgrid_instance': mock_sendgrid_instance
    }
```

## Migration from Individual Mocks

### Before (Individual Mocks)

```python
def test_with_individual_mocks(api_client, mocker, access_token):
    """
    Test with individual mocks
    """
    mock_api = mocker.patch('apps.app.actions.external_api')
    mock_api.return_value = {'status': 'success'}
    
    mock_db = mocker.patch('apps.app.actions.database_operation')
    mock_db.return_value = True
    
    # Test logic...
    
    mock_api.assert_called_once()
    mock_db.assert_called_once()
```

### After (Shared Mocks)

```python
@pytest.mark.shared_mocks(lambda mocker: mock_complex_operation_shared_mock(mocker))
def test_with_shared_mocks(api_client, access_token, mock_external_api, mock_db_operation):
    """
    Test with shared mocks
    """
    # Test logic...
    
    mock_external_api.assert_called_once()
    mock_db_operation.assert_called_once()
```

## Benefits

1. **Code Reuse**: Define mocks once, use them across multiple tests
2. **Consistency**: Ensure consistent mocking behavior across tests
3. **Maintainability**: Update mock behavior in one place
4. **Readability**: Tests focus on business logic, not mock setup
5. **Reliability**: Reduce the chance of mock setup errors

## When to Use Shared Mocks

### Use Shared Mocks When:
- The same mocks are used across multiple tests
- You have complex mock setups that are repeated
- You want to ensure consistent behavior across tests
- You're testing similar scenarios with different inputs

### Don't Use Shared Mocks When:
- The mock is only used in one test
- The mock setup is very simple (1-2 lines)
- The mock behavior varies significantly between tests

## Troubleshooting

### Common Issues

1. **Mock not found**: Ensure the mock function returns a dictionary with the expected keys
2. **Import errors**: Check that the mock setup file is properly imported
3. **Mock not called**: Verify that the mock is being applied to the correct import path

### Debugging

```python
@pytest.mark.shared_mocks(lambda mocker: mock_debug_shared_mock(mocker))
def test_debug_mocks(api_client, access_token, **kwargs):
    """
    Debug test to see what mocks are available
    """
    print("Available mocks:", kwargs.keys())
    # Test logic...
```

This guide provides a comprehensive overview of how to use shared mocks in the settings-api project. Follow these patterns to create maintainable and reusable test mocks. 
