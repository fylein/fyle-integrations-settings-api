fixture = {
   "managed_user":{
      "id": 1,
      "external_id": "orTwovfDpEYc",
      "name": "Test User",
      "notification_email": "test@example.com"
   },
   "connections":{
      "result":[
         {
            "id": 1,
            "authorization_status": "success",
            "name": "My SendGrid account"
         },
         {
            "id": 2,
            "authorization_status": "success",
            "name": "My BambooHR account"
         }
      ]
   },
   "orgs":{
      "id": 1,
      "name": "Test Org",
      "fyle_org_id": "orHVw3ikkCxJ",
      "managed_user_id": "1",
      "allow_travelperk": False,
      "allow_gusto": False,
      "is_fyle_connected": True,
      "is_sendgrid_connected": False,
      "cluster_domain": "https://staging.fyle.tech",
      "created_at": "2022-09-27T09:58:51.483072Z",
      "updated_at": "2022-09-27T09:58:51.483135Z",
      "allow_dynamics": False,
      "allow_qbd_direct_integration": False,
      "user": [1]
   },
   "my_profile_admin":{
      "data":{
         "org":{
            "currency": "EUR",
            "domain": "test.fyle.in",
            "id": "orHVw3ikkCxK",
            "name": "Test Org"
         },
         "org_id": "orHVw3ikkCxK",
         "roles": [
            "FYLER",
            "ADMIN"
         ],
         "user": {
            "email": "test@fyle.in",
            "full_name": "Test User",
            "id": "usqywo0f3nBZ"
         },
         "user_id": "usqywo0f3nBZ"
      }
   },
   "users":{
      "count": 1,
      "data":[
         {
            "approver_user_ids": [],
            "approver_users": [],
            "branch_account": "None",
            "branch_ifsc": "None",
            "business_unit": "None",
            "code": "None",
            "cost_center_ids": [],
            "cost_centers": [],
            "created_at": "2020-11-11T10:49:28.590000+00:00",
            "custom_fields": [],
            "department": "None",
            "department_id": "None",
            "has_accepted_invite": True,
            "id": "outanpL7lcv4",
            "is_enabled": True,
            "joined_at": "None",
            "level": "None",
            "level_id": "None",
            "location": "None",
            "mileage_rate_ids": [],
            "mileage_rates": [],
            "mobile": "None",
            "org_id": "or7m5SVD9Rv1",
            "per_diem_rate_ids": [4361],
            "per_diem_rates": [
               {
                  "code": "None",
                  "currency": "USD",
                  "id": 4361,
                  "name": "Per Diem 9"
               }
            ],
            "project_ids": [],
            "projects": [],
            "roles": [
               "OWNER",
               "FYLER",
               "ADMIN",
               "HOD"
            ],
            "special_email": "receipts+owner_0fna@fyle.ai",
            "title": "Admin",
            "updated_at": "2020-11-11T10:49:43.010151+00:00",
            "user": {
               "email": "test@example.com",
               "full_name": "Test User",
               "id": "usG6YgUWBHIG"
            },
            "user_id": "usG6YgUWBHIG"
         }
      ],
      "offset": 0
   }
}

expected_org_response = {
    "id": 1,
    "name": "Test Org",
    "fyle_org_id": "orHVw3ikkCxJ",
    "managed_user_id": "1",
    "allow_travelperk": False,
    "allow_gusto": False,
    "is_fyle_connected": True,
    "is_sendgrid_connected": False,
    "cluster_domain": "https://staging.fyle.tech",
    "created_at": "2022-09-27T09:58:51.483072Z",
    "updated_at": "2022-09-27T09:58:51.483135Z",
    "allow_dynamics": False,
    "allow_qbd_direct_integration": False,
    "user": [1]
}
