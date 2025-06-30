fixture = {
   'bamboohr': {
      "id":1,
      "folder_id":"1231",
      "package_id":"1231",
      "api_token":"seofihsdofighsodifghspdiof",
      "sub_domain":"dummy",
      "webhook_id": "123",
      "private_key": "123",
      "created_at":"2022-11-29T15:39:49.221955Z",
      "updated_at":"2022-11-29T15:41:59.535831Z",
      "org":1,
      "employee_exported_at": "2022-11-29T15:39:49.221955Z",
      "is_credentials_expired": False,
   },
   "configurations": {
      "id":1,
      "org": None,
      "recipe_id": None,
      "recipe_data": None,
      "recipe_status": False,
      "additional_email_options":[{
         "name":"Nilsh",
         "email":"dfoisdfoh@gmail.com"
      }],
      "emails_selected":[
         "ni12lesh[amt1212@gmail.in",
         "ashwin.t@fyle.in"
      ]
   },

   "bamboo_connection": {
      'input': {
         'api_token': 'sample_token',
         'subdomain': 'somesubdomain'
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
    }
}

configuration_data = {
    "additional_email_options": {},
    "emails_selected": [
        {
            "name": "Nilesh",
            "email": "nilesh.p@fyle.in"
        },
    ]
}

bamboo_connection_invalid_payload = {
    'input': {
        'api_token': 'sample_token',
    }
}

bamboo_connection = {
    'input': {
        'api_token': 'sample_token',
        'subdomain': 'somesubdomain'
    }
}

bamboohr_integrations_response = {
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
}

# Email test data
email_template_content = """
<html>
<body>
<h1>Error Importing Employees from Bamboo HR to Fyle</h1>
<p>We encountered errors importing {number_of_employees} employees from BambooHR to Fyle.</p>
<p>Please find the employee details in the attached CSV file.</p>
</body>
</html>
"""

failed_employees_data = [
    {'id': '1', 'name': 'John Doe'},
    {'id': '2', 'name': 'Jane Smith'},
    {'id': '3', 'name': 'Bob Johnson'}
]

admin_email_list = ['admin1@example.com', 'admin2@example.com']

number_of_employees = 3

# Task test data
webhook_payload = {
    'employees': [{
        'id': '123',
        'fields': {
            'firstName': {'value': 'John'},
            'lastName': {'value': 'Doe'},
            'workEmail': {'value': 'john.doe@example.com'},
            'status': {'value': 'Active'},
            'employeeNumber': {'value': 'EMP123'}
        }
    }]
}

# Health check test data
bamboohr_timeoff_success_response = {
    'timeOffTypes': [
        {'id': 1, 'name': 'Vacation'},
        {'id': 2, 'name': 'Sick Leave'}
    ]
}

bamboohr_timeoff_empty_response = {
    'timeOffTypes': []
}

# Sync employees test data
sync_employees_request_data = {}

# Configuration exception test data
invalid_configuration_data = {
    "additional_email_options": "invalid_format",
    "emails_selected": "invalid_format"
}
