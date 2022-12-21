fixture = {
    'bamboohr': {
       "id":1,
       "folder_id":"1231",
       "package_id":"1231",
       "api_token":"seofihsdofighsodifghspdiof",
       "sub_domain":"dummy",
       "created_at":"2022-11-29T15:39:49.221955Z",
       "updated_at":"2022-11-29T15:41:59.535831Z",
       "org":1
    },
    "configurations": {
           "id":1,
           "org": None,
           "recipe_id": None,
           "recipe_data": None,
           "recipe_status": False,
           "additional_email_options":{
              "name":"Nilsh",
              "email":"dfoisdfoh@gmail.com"
           },
           "emails_selected":[
              "ni12lesh[amt1212@gmail.in",
              "ashwin.t@fyle.in"
           ]
        },
    "connections": {
        "result": [
            {"id": 12, "authorization_status": "success", "name": "My SendGrid account"},
            {"id": 13, "authorization_status": "success", "name": "BambooHR Connection"},
            {"id": 14,"authorization_status": "success", "name": "BambooHR Sync Connection"},
        ] 
    },
    "recipes": {
      "result": [
         {
            "id": 3545113,
            "user_id": 910391,
            "name": "BambooHr Cron Job",
            "created_at": "2022-12-16T10:01:06.655-08:00",
            "updated_at": "2022-12-16T10:01:06.655-08:00",
            "copy_count": 1,
            "trigger_application": "bamboohr",
            "action_applications": [
                "fyle_prod_connector_910391_1671213665",
                "sendgrid"
            ],
            "applications": [
                "bamboohr",
                "fyle_prod_connector_910391_1671213665",
                "sendgrid"
            ],
            "description": "When there is a trigger event, do action",
            "parameters_schema": [],
            "parameters": {},
            "webhook_url": False,
            "folder_id": 1699404,
            "running": False,
            "job_succeeded_count": 0,
            "job_failed_count": 0,
            "lifetime_task_count": 0,
            "last_run_at": None,
            "stopped_at": None,
            "version_no": 1,
            "stop_cause": None,
            "config": [
                {
                    "keyword": "application",
                    "provider": "bamboohr",
                    "skip_validation": False,
                    "name": "bamboohr",
                    "account_id": 1176946
                },
                {
                    "keyword": "application",
                    "provider": "fyle_prod_connector_910391_1671213665",
                    "skip_validation": False,
                    "name": "fyle_prod_connector_910391_1671213665",
                    "account_id": 1176948
                },
                {
                    "keyword": "application",
                    "provider": "sendgrid",
                    "skip_validation": False,
                    "name": "sendgrid",
                    "account_id": 1176949
                }
            ],
            "code": "{\"number\":0,\"provider\":\"bamboohr\",\"name\":\"updated_employee\",\"as\":\"6761c014\",\"title\":null,\"description\":null,\"keyword\":\"trigger\",\"dynamicPickListSelection\":{},\"toggleCfg\":{\"flag\":true},\"input\":{\"flag\":\"true\"},\"extended_output_schema\":[{\"control_type\":\"text\",\"label\":\"NIN\",\"name\":\"customNIN1\",\"optional\":true,\"type\":\"string\"},{\"control_type\":\"select\",\"label\":\"SecondaryLanguage\",\"name\":\"customSecondaryLanguage1\",\"optional\":true,\"pick_list\":[[\"French\",\"French\"],[\"German\",\"German\"],[\"Japanese\",\"Japanese\"],[\"Mandarin\",\"Mandarin\"],[\"Spanish\",\"Spanish\"]],\"toggle_field\":{\"control_type\":\"text\",\"label\":\"SecondaryLanguage\",\"toggle_hint\":\"Entercustomvalue\",\"optional\":true,\"type\":\"string\",\"name\":\"customSecondaryLanguage1\"},\"toggle_hint\":\"Selectfromlist\",\"type\":\"string\"},{\"control_type\":\"select\",\"label\":\"Shirtsize\",\"name\":\"customShirtsize\",\"optional\":true,\"pick_list\":[[\"1.Small\",\"1.Small\"],[\"2.Medium\",\"2.Medium\"],[\"3.Large\",\"3.Large\"],[\"4.XLarge\",\"4.XLarge\"],[\"5.XXLarge\",\"5.XXLarge\"]],\"toggle_field\":{\"control_type\":\"text\",\"label\":\"Shirtsize\",\"toggle_hint\":\"Entercustomvalue\",\"optional\":true,\"type\":\"string\",\"name\":\"customShirtsize\"},\"toggle_hint\":\"Selectfromlist\",\"type\":\"string\"},{\"control_type\":\"text\",\"label\":\"TaxFileNumber\",\"name\":\"customTaxFileNumber1\",\"optional\":true,\"type\":\"string\"}],\"block\":[{\"number\":1,\"keyword\":\"try\",\"dynamicPickListSelection\":{},\"toggleCfg\":{},\"input\":{},\"block\":[{\"number\":2,\"keyword\":\"if\",\"dynamicPickListSelection\":{},\"toggleCfg\":{},\"input\":{\"type\":\"compound\",\"operand\":\"and\",\"conditions\":[{\"operand\":\"present\",\"lhs\":\"#{_('data.bamboohr.6761c014.supervisorEId')}\",\"rhs\":\"\",\"uuid\":\"condition-79dc736e-21b3-4f53-bcd3-eafef8a76362\"}]},\"block\":[{\"number\":3,\"provider\":\"bamboohr\",\"name\":\"get_employee_by_id\",\"as\":\"e5cf843b\",\"title\":null,\"description\":null,\"keyword\":\"action\",\"dynamicPickListSelection\":{},\"toggleCfg\":{},\"input\":{\"id\":\"#{_('data.bamboohr.6761c014.supervisorEId')}\"},\"extended_output_schema\":[{\"control_type\":\"text\",\"label\":\"NIN\",\"name\":\"customNIN1\",\"optional\":true,\"type\":\"string\"},{\"control_type\":\"select\",\"label\":\"SecondaryLanguage\",\"name\":\"customSecondaryLanguage1\",\"optional\":true,\"pick_list\":[[\"French\",\"French\"],[\"German\",\"German\"],[\"Japanese\",\"Japanese\"],[\"Mandarin\",\"Mandarin\"],[\"Spanish\",\"Spanish\"]],\"toggle_field\":{\"control_type\":\"text\",\"label\":\"SecondaryLanguage\",\"toggle_hint\":\"Entercustomvalue\",\"optional\":true,\"type\":\"string\",\"name\":\"customSecondaryLanguage1\"},\"toggle_hint\":\"Selectfromlist\",\"type\":\"string\"},{\"control_type\":\"select\",\"label\":\"Shirtsize\",\"name\":\"customShirtsize\",\"optional\":true,\"pick_list\":[[\"1.Small\",\"1.Small\"],[\"2.Medium\",\"2.Medium\"],[\"3.Large\",\"3.Large\"],[\"4.XLarge\",\"4.XLarge\"],[\"5.XXLarge\",\"5.XXLarge\"]],\"toggle_field\":{\"control_type\":\"text\",\"label\":\"Shirtsize\",\"toggle_hint\":\"Entercustomvalue\",\"optional\":true,\"type\":\"string\",\"name\":\"customShirtsize\"},\"toggle_hint\":\"Selectfromlist\",\"type\":\"string\"},{\"control_type\":\"text\",\"label\":\"TaxFileNumber\",\"name\":\"customTaxFileNumber1\",\"optional\":true,\"type\":\"string\"}],\"uuid\":\"587d07c1-2d4e-473a-853a-f768b441bd7c\"},{\"number\":4,\"provider\":\"fyle_prod_connector_910391_1671213665\",\"name\":\"search_employee\",\"as\":\"d02a328f\",\"title\":null,\"description\":null,\"keyword\":\"action\",\"dynamicPickListSelection\":{},\"toggleCfg\":{},\"input\":{\"email\":\"='eq.'+_('data.bamboohr.e5cf843b.workEmail')\"},\"extended_output_schema\":[{\"label\":\"Employees\",\"name\":\"data\",\"of\":\"object\",\"optional\":true,\"properties\":[{\"control_type\":\"number\",\"label\":\"Count\",\"parse_output\":\"float_conversion\",\"optional\":true,\"type\":\"number\",\"name\":\"count\"},{\"name\":\"data\",\"type\":\"array\",\"of\":\"object\",\"label\":\"Data\",\"optional\":true,\"properties\":[{\"control_type\":\"text\",\"label\":\"Branchaccount\",\"optional\":true,\"type\":\"string\",\"name\":\"branch_account\"},{\"control_type\":\"text\",\"label\":\"Branchifsc\",\"optional\":true,\"type\":\"string\",\"name\":\"branch_ifsc\"},{\"control_type\":\"text\",\"label\":\"Businessunit\",\"optional\":true,\"type\":\"string\",\"name\":\"business_unit\"},{\"control_type\":\"text\",\"label\":\"Code\",\"optional\":true,\"type\":\"string\",\"name\":\"code\"},{\"control_type\":\"text\",\"label\":\"Createdat\",\"render_input\":\"date_time_conversion\",\"parse_output\":\"date_time_conversion\",\"optional\":true,\"type\":\"date_time\",\"name\":\"created_at\"},{\"control_type\":\"text\",\"label\":\"Department\",\"optional\":true,\"type\":\"string\",\"name\":\"department\"},{\"control_type\":\"text\",\"label\":\"DepartmentID\",\"optional\":true,\"type\":\"string\",\"name\":\"department_id\"},{\"control_type\":\"text\",\"label\":\"Hasacceptedinvite\",\"parse_output\":{},\"render_input\":{},\"toggle_hint\":\"Selectfromoptionlist\",\"toggle_field\":{\"label\":\"Hasacceptedinvite\",\"control_type\":\"text\",\"toggle_hint\":\"Usecustomvalue\",\"type\":\"boolean\",\"name\":\"has_accepted_invite\"},\"optional\":true,\"type\":\"number\",\"name\":\"has_accepted_invite\"},{\"control_type\":\"text\",\"label\":\"ID\",\"optional\":true,\"type\":\"string\",\"name\":\"id\"},{\"control_type\":\"text\",\"label\":\"Isenabled\",\"parse_output\":{},\"render_input\":{},\"toggle_hint\":\"Selectfromoptionlist\",\"toggle_field\":{\"label\":\"Isenabled\",\"control_type\":\"text\",\"toggle_hint\":\"Usecustomvalue\",\"type\":\"boolean\",\"name\":\"is_enabled\"},\"optional\":true,\"type\":\"number\",\"name\":\"is_enabled\"},{\"control_type\":\"text\",\"label\":\"Joinedat\",\"render_input\":\"date_time_conversion\",\"parse_output\":\"date_time_conversion\",\"optional\":true,\"type\":\"date_time\",\"name\":\"joined_at\"},{\"control_type\":\"text\",\"label\":\"Level\",\"optional\":true,\"type\":\"string\",\"name\":\"level\"},{\"control_type\":\"text\",\"label\":\"LevelID\",\"optional\":true,\"type\":\"string\",\"name\":\"level_id\"},{\"control_type\":\"text\",\"label\":\"Location\",\"optional\":true,\"type\":\"string\",\"name\":\"location\"},{\"control_type\":\"text\",\"label\":\"Mobile\",\"optional\":true,\"type\":\"string\",\"name\":\"mobile\"},{\"control_type\":\"text\",\"label\":\"OrgID\",\"optional\":true,\"type\":\"string\",\"name\":\"org_id\"},{\"name\":\"roles\",\"type\":\"array\",\"of\":\"string\",\"label\":\"Roles\",\"optional\":true},{\"control_type\":\"text\",\"label\":\"Specialemail\",\"optional\":true,\"type\":\"string\",\"name\":\"special_email\"},{\"control_type\":\"text\",\"label\":\"Title\",\"optional\":true,\"type\":\"string\",\"name\":\"title\"},{\"control_type\":\"text\",\"label\":\"Updatedat\",\"render_input\":\"date_time_conversion\",\"parse_output\":\"date_time_conversion\",\"optional\":true,\"type\":\"date_time\",\"name\":\"updated_at\"},{\"label\":\"User\",\"optional\":true,\"type\":\"object\",\"name\":\"user\",\"properties\":[{\"control_type\":\"text\",\"label\":\"Email\",\"optional\":true,\"type\":\"string\",\"name\":\"email\"},{\"control_type\":\"text\",\"label\":\"Fullname\",\"optional\":true,\"type\":\"string\",\"name\":\"full_name\"},{\"control_type\":\"text\",\"label\":\"ID\",\"optional\":true,\"type\":\"string\",\"name\":\"id\"}]},{\"control_type\":\"text\",\"label\":\"UserID\",\"optional\":true,\"type\":\"string\",\"name\":\"user_id\"}]},{\"control_type\":\"number\",\"label\":\"Offset\",\"parse_output\":\"float_conversion\",\"optional\":true,\"type\":\"number\",\"name\":\"offset\"}],\"type\":\"array\"}],\"uuid\":\"55913e43-d3fd-451e-837a-445246be5c7f\"}],\"uuid\":\"499d0a9a-7aec-4b07-a106-30ca7589545a\"},{\"number\":5,\"provider\":\"fyle_prod_connector_910391_1671213665\",\"name\":\"create_employees_in_fyle\",\"as\":\"07f04431\",\"title\":null,\"description\":null,\"keyword\":\"action\",\"dynamicPickListSelection\":{},\"toggleCfg\":{},\"input\":{\"data\":{\"user_email\":\"#{_('data.bamboohr.6761c014.workEmail')}\",\"user_full_name\":\"#{_('data.bamboohr.6761c014.displayName')}\",\"title\":\"#{_('data.bamboohr.6761c014.jobTitle')}\",\"location\":\"#{_('data.bamboohr.6761c014.location')}\",\"is_enabled\":\"=_('data.bamboohr.6761c014.status').include?(\\\"Active\\\")\",\"approver_emails\":\"=_('data.fyle_prod_connector_910391_1671213665.d02a328f.data').present??[_('data.bamboohr.e5cf843b.workEmail')]:[]\"}},\"visible_config_fields\":[\"data\",\"data.is_enabled\",\"data.user_full_name\",\"data.user_email\",\"data.title\",\"data.location\",\"data.approver_emails\"],\"uuid\":\"36320f70-4509-46fe-80c3-fd89ac93a0dd\",\"skip\":false},{\"number\":6,\"as\":\"86be96e2\",\"keyword\":\"catch\",\"dynamicPickListSelection\":{},\"toggleCfg\":{},\"input\":{\"max_retry_count\":\"0\",\"retry_interval\":\"2\"},\"block\":[{\"number\":7,\"provider\":\"sendgrid\",\"name\":\"send_email\",\"as\":\"2c55fabe\",\"keyword\":\"action\",\"dynamicPickListSelection\":{},\"toggleCfg\":{},\"input\":{\"from\":{\"email\":\"notifications-staging@fylehq.com\"},\"subject\":\"FyleBambooHRIntegrations\",\"content\":{\"type\":\"text/plain\",\"value\":\"=\\\"SomethingUnexpectedhappenedwhileimportingemployeename\\\"+_('data.bamboohr.6761c014.displayName')+\\\"andemail\\\"+_('data.bamboohr.6761c014.workEmail')+\\\"pleasecontactsupportteam.\\\"\"},\"personalizations\":[{\"to\":[{\"email\":\"test\"}]}]},\"uuid\":\"93f8d230-00ae-456e-891c-653daa656dea\"}],\"uuid\":\"d6e76e57-08a2-4d26-a7c1-d74c92709d06\"}],\"uuid\":\"14f5a93e-8d8a-4659-8dba-ded9b816b173\"}],\"uuid\":\"9facdee0-dff2-4a3c-bf60-06265ca8a599\"}"
        },
      ]
    }
}