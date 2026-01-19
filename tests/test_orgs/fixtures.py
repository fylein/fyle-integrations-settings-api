# Static test data for mocks
fyle_admin_response = {
    'data': {
        'user': {'email': 'admin@fyle.in', 'id': 'admin123'},
        'org': {'id': 'orHVw3ikkCxJ', 'name': 'Anagha Org'}
    }
}

fyle_admin_simple_response = {
    'data': {
        'user': {'email': 'admin@fyle.in', 'id': 'admin123'}
    }
}

platform_employees_response = [
    {
        'data': [
            {'user': {'email': 'abc@ac.com', 'full_name': 'abc'}}
        ]
    }
]

platform_employees_simple_response = [
    {'email': 'abc@ac.com', 'name': 'abc'}
]

fixture = {
   "managed_user":{
      "id":890744,
      "external_id":"orTwovfDpEYc",
      "name":"None",
      "notification_email":"None"
   },
   "connections":{
      "result":[
         {
            "id":12,
            "authorization_status":"success",
            "name":"My SendGrid account"
         },
         {
            "id":13,
            "authorization_status":"success",
            "name":"My BambooHR account"
         },
         {
            "id":14,
            "authorization_status":"success",
            "name":"Bamboo HR"
         },
         {
            "id":15,
            "authorization_status":"success",
            "name":"Fyle Connection"
         },
         {
            "id":16,
            "authorization_status":"success",
            "name":"Fyle Common Connection"
         },
         {
            "id":17,
            "authorization_status":"success",
            "name":"Sendgrid Common Connection"
         }
      ]
   },
   "orgs":{
      "id":2,
      "name":"Anagha Org",
      "fyle_org_id":"orHVw3ikkCxJ",
      "managed_user_id":"2",
      "allow_travelperk": True,
      "allow_gusto": True,
      "is_fyle_connected":"true",
      "is_sendgrid_connected":"false",
      "is_org_rebranded": False,
      "cluster_domain":"https://staging.fyle.tech",
      "created_at":"2022-09-27T09:58:51.483072Z",
      "updated_at":"2022-09-27T09:58:51.483135Z",
      "allow_travelperk": False,
      "allow_gusto": False,
      "allow_dynamics": False,
      "allow_bamboohr": False,
      "allow_qbd_direct_integration": False,
      "user":[
         2
      ]
   },
   "my_profile_admin":{
      "data":{
         "org":{
            "currency":"EUR",
            "domain":"aafyle.in",
            "id":"orHVw3ikkCxK",
            "name":"Ashwin Org"
         },
         "org_id":"orHVw3ikkCxK",
         "roles":[
            "FYLER",
            "ADMIN"
         ],
         "user":{
            "email":"ashwin.t+1@fyle.in",
            "full_name":"Joannaa",
            "id":"usqywo0f3nBZ"
         },
         "user_id":"usqywo0f3nBZ"
      }
   },
   "users":{
      "count":1,
      "data":[
         {
            "approver_user_ids":[

            ],
            "approver_users":[

            ],
            "branch_account":"None",
            "branch_ifsc":"None",
            "business_unit":"None",
            "code":"None",
            "cost_center_ids":[

            ],
            "cost_centers":[

            ],
            "created_at":"2020-11-11T10:49:28.590000+00:00",
            "custom_fields":[

            ],
            "department":"None",
            "department_id":"None",
            "has_accepted_invite":True,
            "id":"outanpL7lcv4",
            "is_enabled":True,
            "joined_at":"None",
            "level":"None",
            "level_id":"None",
            "location":"None",
            "mileage_rate_ids":[

            ],
            "mileage_rates":[

            ],
            "mobile":"None",
            "org_id":"or7m5SVD9Rv1",
            "per_diem_rate_ids":[
               4361
            ],
            "per_diem_rates":[
               {
                  "code":"None",
                  "currency":"USD",
                  "id":4361,
                  "name":"Per Diem 9"
               }
            ],
            "project_ids":[

            ],
            "projects":[

            ],
            "roles":[
               "OWNER",
               "FYLER",
               "ADMIN",
               "HOD"
            ],
            "special_email":"receipts+owner_0fna@fyle.ai",
            "title":"Admin",
            "updated_at":"2020-11-11T10:49:43.010151+00:00",
            "user":{
               "email":"abc@ac.com",
               "full_name":"abc",
               "id":"usG6YgUWBHIG"
            },
            "user_id":"usG6YgUWBHIG"
         }
      ],
      "offset":0
   }
}
