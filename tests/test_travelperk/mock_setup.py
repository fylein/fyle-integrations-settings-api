"""
Mock setup functions for TravelPerk tests
"""

from io import BytesIO
from .fixtures import (
    advance_setting_payload, 
    integrations_response, 
    profile_mapping_payload, 
    profile_mapping_response,
    dummy_org_id,
    dummy_org_name,
    test_refresh_token,
    test_employee_email,
    nonexistent_employee_email,
    test_amount,
    test_card_id,
    test_url,
    test_presigned_url,
    test_file_content,
    employee_query_params,
    employee_query_params_nonexistent,
    transaction_query_params,
    file_upload_headers,
    webhook_create_data,
    webhook_response_data,
    webhook_delete_response,
    invoice_profile_data,
    invoice_profile_no_country,
    invoice_profile_no_currency,
    test_webhook_subscription_id,
    test_refresh_token_updated
)


def mock_platform_connector(mocker):
    """
    Mock platform connector for TravelPerk tests
    """
    mock_connector = mocker.MagicMock()
    mock_connector.connection.v1.spender.my_profile.get.return_value = {
        'data': {
            'user': {
                'email': 'janedoe@gmail.com',
                'id': '1234'
            }
        }
    }
    
    mocker.patch('apps.users.helpers.PlatformConnector', return_value=mock_connector)
    return mock_connector


def mock_travelperk_connector_disconnect(mocker):
    """
    Mock TravelPerk connector disconnect
    """
    mock_connector = mocker.MagicMock()
    mock_connector.delete_webhook_connection.return_value = {'message': 'success'}
    mocker.patch('apps.travelperk.views.TravelperkConnector', return_value=mock_connector)
    return mock_connector


def mock_travelperk_connector_connect(mocker):
    """
    Mock TravelPerk connector connect
    """
    mock_connector = mocker.MagicMock()
    mock_connector.create_webhook.return_value = {'id': 123}
    mocker.patch('apps.travelperk.views.TravelperkConnector', return_value=mock_connector)
    return mock_connector


def mock_get_refresh_token(mocker):
    """
    Mock get refresh token
    """
    mock_token = mocker.MagicMock()
    mock_token.return_value = 'dummy_refresh_token'
    mocker.patch('apps.travelperk.views.get_refresh_token_using_auth_code', mock_token)
    return mock_token


def mock_test_get_profile_mappings_case_1(mocker):
    """
    Mock setup for test_get_profile_mappings_case_1
    """
    return {
        'profile_mapping_payload': profile_mapping_payload,
        'profile_mapping_response': profile_mapping_response
    }


def mock_test_get_advanced_settings_case_1(mocker):
    """
    Mock setup for test_get_advanced_settings_case_1
    """
    return {
        'advance_setting_payload': advance_setting_payload,
        'integrations_response': integrations_response
    }


def mock_travelperk_shared_mock(mocker):
    """
    Shared mock setup for TravelPerk tests
    """
    mock_platform = mocker.MagicMock()
    mock_platform.connection.v1.spender.my_profile.get.return_value = {
        'data': {
            'user': {
                'email': 'janedoe@gmail.com',
                'id': '1234'
            }
        }
    }
    
    mock_travelperk_connector = mocker.MagicMock()
    mock_travelperk_connector.create_webhook.return_value = {'id': 123}
    mock_travelperk_connector.delete_webhook_connection.return_value = {'message': 'success'}
    
    mocker.patch('apps.travelperk.views.PlatformConnector', return_value=mock_platform)
    mocker.patch('apps.travelperk.views.TravelperkConnector', return_value=mock_travelperk_connector)
    mocker.patch(
        'apps.travelperk.views.get_refresh_token_using_auth_code',
        return_value={'123e3rwer'}
    )
    
    return {
        'platform_connector': mock_platform,
        'travelperk_connector': mock_travelperk_connector,
        'create_webhook': mock_travelperk_connector.create_webhook,
        'delete_webhook_connection': mock_travelperk_connector.delete_webhook_connection,
        'get_my_profile': mock_platform.connection.v1.spender.my_profile.get,
    } 


def mock_construct_expense_payload_case_1(mocker):
    mock_get_category_id = mocker.patch('apps.travelperk.actions.get_category_id', return_value='1234')
    return {'get_category_id': mock_get_category_id}


def mock_create_invoice_lineitems_case_1(mocker):
    mock_connector = mocker.MagicMock()
    mock_connector.v1.admin.employees.list.return_value = {'data': [{'user': {'email': 'johndoe@gmail.com'}}]}
    mock_connector.v1.admin.expenses.post.return_value = {'data': {'id': '123'}}

    mock_construct_file_ids = mocker.patch(
        'apps.travelperk.actions.construct_file_ids',
        return_value=['123']
    )
    mock_platform = mocker.patch(
        'apps.orgs.utils.Platform',
        return_value=mock_connector
    )
    return {
        'construct_file_ids': mock_construct_file_ids,
        'platform': mock_platform,
        'mock_connector': mock_connector
    }


def mock_attach_reciept_to_expense_case_1(mocker):
    """
    Mock setup for test_attach_reciept_to_expense_case_1
    """
    mock_platform_connection = mocker.MagicMock()
    mock_platform_connection.v1.spender.files.create_file.return_value = {
        'data': {'id': 'test_file_id'}
    }
    mock_platform_connection.v1.spender.files.generate_file_urls.return_value = {
        'data': {'upload_url': 'https://test-upload-url.com'}
    }
    mock_platform_connection.v1.spender.expenses.attach_receipt.return_value = True
    
    mock_download_file = mocker.patch('apps.travelperk.actions.download_file', return_value=b'test_file_content')
    mock_upload_to_s3 = mocker.patch('apps.travelperk.actions.upload_to_s3_presigned_url', return_value=None)
    
    return {
        'platform_connection': mock_platform_connection,
        'download_file': mock_download_file,
        'upload_to_s3': mock_upload_to_s3
    }


def mock_test_create_expense_in_fyle_v2_case_1(mocker):
    """
    Mock setup for test_create_expense_in_fyle_v2_case_1
    """
    mock_platform_connection = mocker.MagicMock()
    mock_platform_connection.v1.admin.categories.list.return_value = {
        'count': 1,
        'data': [{'id': 'test_category_id'}]
    }
    mock_platform_connection.v1.spender.expenses.post.return_value = {
        'data': {'id': 'test_expense_id'}
    }
    
    mock_create_fyle_connection = mocker.patch(
        'apps.travelperk.actions.create_fyle_connection',
        return_value=mock_platform_connection
    )
    
    mock_attach_reciept_to_expense = mocker.patch(
        'apps.travelperk.actions.attach_reciept_to_expense',
        return_value=None
    )
    
    return {
        'platform_connection': mock_platform_connection,
        'create_fyle_connection': mock_create_fyle_connection,
        'attach_reciept_to_expense': mock_attach_reciept_to_expense
    }


def mock_get_category_id_case_1(mocker):
    """
    Mock setup for test_get_category_id_case_1
    """
    mock_advanced_settings = mocker.MagicMock()
    mock_advanced_settings.category_mappings = {
        'Flights': {'id': '228953', 'name': 'Customer Deposits'}
    }
    mock_advanced_settings.default_category_id = '228952'
    
    return {
        'advanced_settings': mock_advanced_settings
    }


def mock_create_expense_against_employee_case_1(mocker):
    """
    Mock setup for test_create_expense_against_employee_case_1
    """
    mock_create_invoice_lineitems = mocker.patch(
        'apps.travelperk.actions.create_invoice_lineitems',
        return_value=mocker.MagicMock()
    )
    
    return {
        'create_invoice_lineitems': mock_create_invoice_lineitems
    }


def mock_test_create_expense_in_fyle_case_1(mocker):
    """
    Mock setup for test_create_expense_in_fyle_case_1
    """
    mock_create_expense_against_employee = mocker.patch(
        'apps.travelperk.actions.create_expense_against_employee',
        return_value=None
    )
    
    mock_create_expense_in_fyle_v2 = mocker.patch(
        'apps.travelperk.actions.create_expense_in_fyle_v2',
        return_value=None
    )
    
    return {
        'create_expense_against_employee': mock_create_expense_against_employee,
        'create_expense_in_fyle_v2': mock_create_expense_in_fyle_v2
    }


def mock_add_travelperk_to_integrations_case_1(mocker):
    """
    Mock setup for test_add_travelperk_to_integrations_case_1
    """
    mock_settings = mocker.patch('apps.travelperk.actions.settings')
    mock_settings.FYLE_CLIENT_ID = 'dummy_client_id'
    
    return {
        'settings': mock_settings
    }


def mock_deactivate_travelperk_integration_case_1(mocker):
    """
    Mock setup for test_deactivate_travelperk_integration_case_1
    """
    mock_datetime = mocker.patch('apps.travelperk.actions.datetime')
    mock_datetime.now.return_value = '2024-01-01T00:00:00Z'
    
    return {
        'datetime': mock_datetime
    }


def mock_test_deactivate_travelperk_integration_case_2(mocker):
    """
    Mock setup for test_deactivate_travelperk_integration_case_2
    """
    return {}


def mock_test_disconnect_travelperk_case_2(mocker):
    mock_travelperk_connector = mocker.patch('apps.travelperk.views.TravelperkConnector')
    mock_travelperk_connector.side_effect = AttributeError("'NoneType' object has no attribute 'refresh_token'")
    
    return {
        'travelperk_connector': mock_travelperk_connector
    }


def mock_test_connect_travelperk_case_2(mocker):
    """
    Mock setup for test_connect_travelperk_case_2
    """
    mock_get_refresh_token = mocker.patch(
        'apps.travelperk.helpers.get_refresh_token_using_auth_code'
    )
    mock_get_refresh_token.side_effect = Exception('Invalid code')
    
    return {
        'get_refresh_token': mock_get_refresh_token
    }


def mock_test_webhook_case_1(mocker):
    mock_hmac = mocker.patch('hmac.new')
    mock_hmac.return_value.hexdigest.return_value = 'test_signature'
    
    mock_invoice_create = mocker.patch('apps.travelperk.views.Invoice.create_or_update_invoices')
    mock_invoice_create.return_value = mocker.MagicMock()
    
    mock_lineitem_create = mocker.patch('apps.travelperk.views.InvoiceLineItem.create_or_update_invoice_lineitems')
    mock_lineitem_create.return_value = [mocker.MagicMock()]
    
    mock_async_task = mocker.patch('apps.travelperk.views.async_task')
    
    return {
        'hmac': mock_hmac,
        'invoice_create': mock_invoice_create,
        'lineitem_create': mock_lineitem_create,
        'async_task': mock_async_task
    }


def mock_test_sync_payment_profiles_case_1(mocker):
    mock_sync_profiles = mocker.patch('apps.travelperk.serializers.SyncPaymentProfileSerializer.sync_payment_profiles')
    mock_sync_profiles.return_value = [{'profile_name': 'Test Profile'}]
    
    return {
        'sync_profiles': mock_sync_profiles
    }


def mock_test_validate_healthy_token_case_1(mocker):
    mock_travelperk_connector = mocker.patch('apps.travelperk.views.TravelperkConnector')
    mock_connector_instance = mocker.MagicMock()
    mock_connector_instance.connection.users.me.return_value = {
        'id': 'user_123',
        'email': 'test@example.com'
    }
    mock_travelperk_connector.return_value = mock_connector_instance
    
    return {
        'travelperk_connector': mock_travelperk_connector,
        'connector_instance': mock_connector_instance
    }


def mock_test_get_refresh_token_case_1(mocker):
    mock_requests_post = mocker.patch('apps.travelperk.helpers.requests.post')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.text = f'{{"refresh_token": "{test_refresh_token}"}}'
    mock_requests_post.return_value = mock_response
    
    # Mock the credential update/create that happens in the actual function
    mock_update_or_create = mocker.patch('apps.travelperk.models.TravelperkCredential.objects.update_or_create')
    mock_credential = mocker.MagicMock()
    mock_update_or_create.return_value = (mock_credential, True)
    
    return {
        'requests_post': mock_requests_post,
        'update_or_create': mock_update_or_create,
        'credential': mock_credential
    }


def mock_test_get_refresh_token_case_2(mocker):
    mock_requests_post = mocker.patch('apps.travelperk.helpers.requests.post')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 400
    mock_requests_post.return_value = mock_response
    
    return {
        'requests_post': mock_requests_post
    }


def mock_test_download_file_case_1(mocker):
    mock_requests_get = mocker.patch('apps.travelperk.helpers.requests.get')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.content = test_file_content
    mock_requests_get.return_value = mock_response
    
    return {
        'requests_get': mock_requests_get
    }


def mock_test_download_file_case_2(mocker):
    mock_requests_get = mocker.patch('apps.travelperk.helpers.requests.get')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response
    
    return {
        'requests_get': mock_requests_get
    }


def mock_test_upload_to_s3_case_1(mocker):
    mock_requests_put = mocker.patch('apps.travelperk.helpers.requests.put')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_requests_put.return_value = mock_response
    
    return {
        'requests_put': mock_requests_put
    }


def mock_test_get_employee_email_case_1(mocker):
    mock_platform_connection = mocker.MagicMock()
    mock_platform_connection.v1.admin.employees.list.return_value = {
        'data': [{'user': {'email': test_employee_email}}]
    }
    
    return {
        'platform_connection': mock_platform_connection
    }


def mock_test_get_employee_email_case_2(mocker):
    mock_platform_connection = mocker.MagicMock()
    mock_platform_connection.v1.admin.employees.list.return_value = {
        'data': []
    }
    
    return {
        'platform_connection': mock_platform_connection
    }


def mock_test_check_transaction_case_1(mocker):
    mock_expense = mocker.MagicMock()
    mock_expense.expense_date = '2024-01-01'
    
    mock_platform_connection = mocker.MagicMock()
    mock_platform_connection.v1.admin.corporate_card_transactions.list.return_value = {
        'data': [{'id': 'transaction_123', 'amount': test_amount}]
    }
    
    return {
        'expense': mock_expense,
        'platform_connection': mock_platform_connection
    }


def mock_test_get_email_from_card_case_1(mocker):
    mock_expense = mocker.MagicMock()
    mock_expense.expense_date = '2024-01-01'
    mock_expense.credit_card_last_4_digits = '1234'
    
    mock_platform_connection = mocker.MagicMock()
    
    mock_platform_connection.v1.admin.corporate_cards.list.return_value = {
        'data': [{'user_id': 'user_123', 'id': 'card_123'}]
    }
    
    mock_platform_connection.v1.admin.corporate_card_transactions.list.return_value = {
        'data': []
    }
    
    mock_platform_connection.v1.admin.employees.list.return_value = {
        'data': [{'user': {'email': test_employee_email}}]
    }
    
    return {
        'expense': mock_expense,
        'platform_connection': mock_platform_connection
    }


def mock_test_get_email_from_card_case_2(mocker):
    mock_expense = mocker.MagicMock()
    mock_expense.expense_date = '2024-01-01'
    mock_expense.credit_card_last_4_digits = '1234'
    
    mock_check_transaction = mocker.patch(
        'apps.travelperk.helpers.check_for_transaction_in_fyle',
        return_value=[]
    )
    
    mock_platform_connection = mocker.MagicMock()
    mock_platform_connection.v1.admin.corporate_cards.list.return_value = {
        'data': []
    }
    
    return {
        'expense': mock_expense,
        'platform_connection': mock_platform_connection,
        'check_transaction': mock_check_transaction
    }


def mock_test_construct_file_ids_case_1(mocker):
    mock_platform_connection = mocker.MagicMock()
    mock_platform_connection.v1.spender.files.create_file.return_value = {
        'data': {'id': 'file_123'}
    }
    mock_platform_connection.v1.spender.files.generate_file_urls.return_value = {
        'data': {'upload_url': test_presigned_url}
    }
    
    mock_download_file = mocker.patch('apps.travelperk.helpers.download_file')
    mock_download_file.return_value = BytesIO(test_file_content)
    
    mock_upload_to_s3 = mocker.patch('apps.travelperk.helpers.upload_to_s3_presigned_url')
    
    return {
        'platform_connection': mock_platform_connection,
        'download_file': mock_download_file,
        'upload_to_s3': mock_upload_to_s3
    } 


# TravelPerk Connector Mock Setup Functions

def mock_test_travelperk_connector_init_case_1(mocker):
    mock_travelperk_class = mocker.patch('apps.travelperk.connector.Travelperk')
    mock_travelperk_instance = mocker.MagicMock()
    mock_travelperk_instance.refresh_token = test_refresh_token_updated
    mock_travelperk_class.return_value = mock_travelperk_instance
    
    return {
        'travelperk_class': mock_travelperk_class,
        'travelperk_instance': mock_travelperk_instance
    }


def mock_test_connector_create_webhook_case_1(mocker):
    mock_travelperk_class = mocker.patch('apps.travelperk.connector.Travelperk')
    mock_travelperk_instance = mocker.MagicMock()
    mock_travelperk_instance.refresh_token = test_refresh_token_updated
    mock_travelperk_instance.webhooks.create.return_value = webhook_response_data
    mock_travelperk_class.return_value = mock_travelperk_instance
    
    # Mock the TravelPerk update that happens in the actual function
    mock_travelperk_update = mocker.patch('apps.travelperk.models.TravelPerk.objects.update_or_create')
    
    return {
        'travelperk_class': mock_travelperk_class,
        'travelperk_instance': mock_travelperk_instance,
        'travelperk_update': mock_travelperk_update
    }


def mock_test_connector_create_webhook_case_2(mocker):
    mock_travelperk_class = mocker.patch('apps.travelperk.connector.Travelperk')
    mock_travelperk_instance = mocker.MagicMock()
    mock_travelperk_instance.refresh_token = test_refresh_token_updated
    mock_travelperk_instance.webhooks.create.return_value = None
    mock_travelperk_class.return_value = mock_travelperk_instance
    
    return {
        'travelperk_class': mock_travelperk_class,
        'travelperk_instance': mock_travelperk_instance
    }


def mock_test_connector_delete_webhook_case_1(mocker):
    mock_travelperk_class = mocker.patch('apps.travelperk.connector.Travelperk')
    mock_travelperk_instance = mocker.MagicMock()
    mock_travelperk_instance.refresh_token = test_refresh_token_updated
    mock_travelperk_instance.webhooks.delete.return_value = webhook_delete_response
    mock_travelperk_class.return_value = mock_travelperk_instance
    
    return {
        'travelperk_class': mock_travelperk_class,
        'travelperk_instance': mock_travelperk_instance
    }


def mock_test_connector_sync_invoice_profile_case_1(mocker):
    mock_travelperk_class = mocker.patch('apps.travelperk.connector.Travelperk')
    mock_travelperk_instance = mocker.MagicMock()
    mock_travelperk_instance.refresh_token = test_refresh_token_updated
    mock_travelperk_instance.invoice_profiles.get_all_generator.return_value = iter(invoice_profile_data)
    mock_travelperk_class.return_value = mock_travelperk_instance
    
    # Mock the profile mapping update that happens in the actual function
    mock_profile_mapping_update = mocker.patch('apps.travelperk.models.TravelperkProfileMapping.objects.update_or_create')
    
    return {
        'travelperk_class': mock_travelperk_class,
        'travelperk_instance': mock_travelperk_instance,
        'profile_mapping_update': mock_profile_mapping_update
    }


def mock_test_connector_sync_invoice_profile_case_2(mocker):
    mock_travelperk_class = mocker.patch('apps.travelperk.connector.Travelperk')
    mock_travelperk_instance = mocker.MagicMock()
    mock_travelperk_instance.refresh_token = test_refresh_token_updated
    mock_travelperk_instance.invoice_profiles.get_all_generator.return_value = iter([invoice_profile_no_country])
    mock_travelperk_class.return_value = mock_travelperk_instance
    
    # Mock the profile mapping update that happens in the actual function
    mock_profile_mapping_update = mocker.patch('apps.travelperk.models.TravelperkProfileMapping.objects.update_or_create')
    
    return {
        'travelperk_class': mock_travelperk_class,
        'travelperk_instance': mock_travelperk_instance,
        'profile_mapping_update': mock_profile_mapping_update
    }


def mock_test_connector_sync_invoice_profile_case_3(mocker):
    mock_travelperk_class = mocker.patch('apps.travelperk.connector.Travelperk')
    mock_travelperk_instance = mocker.MagicMock()
    mock_travelperk_instance.refresh_token = test_refresh_token_updated
    mock_travelperk_instance.invoice_profiles.get_all_generator.return_value = iter([invoice_profile_no_currency])
    mock_travelperk_class.return_value = mock_travelperk_instance
    
    # Mock the profile mapping update that happens in the actual function
    mock_profile_mapping_update = mocker.patch('apps.travelperk.models.TravelperkProfileMapping.objects.update_or_create')
    
    return {
        'travelperk_class': mock_travelperk_class,
        'travelperk_instance': mock_travelperk_instance,
        'profile_mapping_update': mock_profile_mapping_update
    }
