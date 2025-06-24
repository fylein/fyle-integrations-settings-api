fixture = {
   'bamboohr': {
      "id": 1,
      "folder_id": "1231",
      "package_id": "1231",
      "api_token": "sample_api_token",
      "sub_domain": "test",
      "webhook_id": "123",
      "private_key": "sample_private_key",
      "created_at": "2022-11-29T15:39:49.221955Z",
      "updated_at": "2022-11-29T15:41:59.535831Z",
      "org": 1,
      "employee_exported_at": "2022-11-29T15:39:49.221955Z",
      "is_credentials_expired": False,
   },
   "bamboo_configuration": {
      "id": 1,
      "org": 1,
      "recipe_id": "recipe_123",
      "recipe_data": {"test": "data"},
      "recipe_status": True,
      "additional_email_options": [{
         "name": "Test User",
         "email": "test@example.com"
      }],
      "emails_selected": [
         "test@example.com",
         "admin@fyle.in"
      ]
   },
   "configurations": {
      "id": 1,
      "org": None,
      "recipe_id": None,
      "recipe_data": None,
      "recipe_status": False,
      "additional_email_options": [{
         "name": "Test User",
         "email": "test@example.com"
      }],
      "emails_selected": [
         "test@example.com",
         "admin@fyle.in"
      ]
   },
   "bamboo_connection": {
      'input': {
         'api_token': 'sample_token',
         'subdomain': 'testsubdomain'
      }
    },
   "bamboo_connection_invalid_payload": {
      'input': {
         'api_token': 'sample_token',
      }
    },
    "integrations_response": {
        "org_id": "orTwovfDpEYc",
        "org_name": "Test org",
        "tpa_id": "dummy",
        "tpa_name": "Fyle BambooHR Integration",
        "type": "HRMS",
        "is_active": True,
        "is_beta": True,
        "connected_at": "2025-01-09T10:08:20.434443Z",
        "disconnected_at": None,
        "updated_at": "2025-01-09T10:08:20.434443Z"
    },
    "employee_payload": {
        'employees': [{
            'id': 123,
            'fields': {
                'firstName': {'value': 'John'},
                'lastName': {'value': 'Doe'},
                'status': {'value': 'Active'}
            }
        }]
    }
}
