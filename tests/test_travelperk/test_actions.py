import pytest
from rest_framework import status
from unittest.mock import MagicMock

from apps.travelperk.actions import (
    construct_expense_payload,
    get_expense_purpose,
    create_invoice_lineitems,
    add_travelperk_to_integrations,
    attach_reciept_to_expense,
    get_category_id,
    create_expense_in_fyle_v2,
    create_expense_against_employee,
    create_expense_in_fyle,
    deactivate_travelperk_integration
)
from apps.travelperk.models import (
    TravelperkAdvancedSetting, 
    ImportedExpenseDetail, 
    Invoice, 
    InvoiceLineItem, 
    TravelperkProfileMapping
)
from apps.orgs.models import Org
from apps.integrations.models import Integration
from tests.helper import dict_compare_keys
from .fixtures import fixture
from .mock_setup import (
    mock_get_category_id,
    mock_construct_file_ids,
    mock_platform_for_actions,
    mock_file_operations,
    mock_fyle_connection,
    mock_employee_operations,
    mock_invoice_operations,
    mock_expense_operations,
    mock_fyle_client_id
)


def test_construct_expense_payload_case_1(mocker, org, invoice_lineitem, advanced_settings, db):
    """
    Test construct_expense_payload function
    Case: constructs payload with valid expense data
    """
    mock_category = mock_get_category_id(mocker)
    payload = construct_expense_payload(org.id, invoice_lineitem, invoice_lineitem.total_amount, ['1321'], 'johndoe@gmail.com')
    assert dict_compare_keys(payload, fixture['payload']) == []


def test_get_expense_purpose_case_1(org, invoice_lineitem, advanced_settings, db):
    """
    Test get_expense_purpose function
    Case: returns formatted expense purpose string
    """
    expense_purpose = get_expense_purpose(org.id, invoice_lineitem)
    assert expense_purpose == '10205 - Flight to West Lisaville - Nilesh Pant - Nilesh Pant - Vueling'


def test_create_invoice_lineitems_case_1(mocker, org_with_credentials, invoice, invoice_lineitem, advanced_settings, db):
    """
    Test create_invoice_lineitems function
    Case: creates invoice lineitem with valid data
    """
    advanced_settings.org = org_with_credentials
    advanced_settings.save()
    
    mock_file_ids = mock_construct_file_ids(mocker)
    mock_platform = mock_platform_for_actions(mocker)
    imported_expense = create_invoice_lineitems(org_with_credentials.id, invoice, invoice_lineitem, 'BOOKER', 120)
    assert imported_expense.expense_id == '123'
    assert imported_expense.file_id == '123'


def test_attach_reciept_to_expense_case_1(mocker, org, db):
    """
    Test attach_reciept_to_expense
    Case: attaches receipt and updates imported_expense
    """
    platform_connection = MagicMock()
    platform_connection.v1.spender.files.create_file.return_value = {'data': {'id': 'file123'}}
    platform_connection.v1.spender.files.generate_file_urls.return_value = {'data': {'upload_url': 'http://upload'}}
    platform_connection.v1.spender.expenses.attach_receipt.return_value = True
    
    # Use shared mock for file operations
    mock_file_ops = mock_file_operations(mocker)
    
    imported_expense = ImportedExpenseDetail.objects.create(expense_id='exp1', org=org)
    invoice = MagicMock()
    invoice.pdf = 'dummy.pdf'
    attach_reciept_to_expense('exp1', invoice, imported_expense, platform_connection)
    imported_expense.refresh_from_db()
    assert imported_expense.file_id == 'file123'
    assert imported_expense.is_reciept_attached is True


def test_attach_reciept_to_expense_case_2(mocker, org, db):
    """
    Test attach_reciept_to_expense
    Case: receipt attachment fails
    """
    platform_connection = MagicMock()
    platform_connection.v1.spender.files.create_file.return_value = {'data': {'id': 'file123'}}
    platform_connection.v1.spender.files.generate_file_urls.return_value = {'data': {'upload_url': 'http://upload'}}
    platform_connection.v1.spender.expenses.attach_receipt.return_value = False
    
    # Use shared mock for file operations
    mock_file_ops = mock_file_operations(mocker)
    
    imported_expense = ImportedExpenseDetail.objects.create(expense_id='exp1', org=org)
    invoice = MagicMock()
    invoice.pdf = 'dummy.pdf'
    attach_reciept_to_expense('exp1', invoice, imported_expense, platform_connection)
    imported_expense.refresh_from_db()
    assert imported_expense.file_id != 'file123'
    assert imported_expense.is_reciept_attached is False


def test_get_category_id_case_default(mocker, org, db):
    """
    Test get_category_id
    Case: category not in mappings, returns default_category_id
    """
    adv = TravelperkAdvancedSetting.objects.create(org=org, default_category_id='default', category_mappings={})
    result = get_category_id(org.id, 'unknown')
    assert result == 'default'


def test_get_category_id_case_mapping(mocker, org, db):
    """
    Test get_category_id
    Case: category in mappings, returns mapped id
    """
    adv = TravelperkAdvancedSetting.objects.create(
        org=org, 
        default_category_id='default', 
        category_mappings={'Cars': {'id': 'carid'}}
    )
    result = get_category_id(org.id, 'car')
    assert result == 'carid'


def test_create_expense_in_fyle_v2_case_1(mocker, org_with_credentials, invoice, invoice_lineitem, db):
    """
    Test create_expense_in_fyle_v2
    Case: creates expense with category mapping
    """
    advanced_settings = TravelperkAdvancedSetting.objects.create(
        org=org_with_credentials,
        default_employee_name='ashwin.t@fyle.in',
        default_employee_id='usqywo0f3nBY',
        default_category_name='Acc. Dep-Leasehold Improvements',
        default_category_id='228952',
        invoice_lineitem_structure='MULTIPLE',
        description_structure=[
            'trip_id',
            'trip_name',
            'traveler_name',
            'booker_name',
            'merchant_name'
        ],
        category_mappings={
            'Cars': {'id': '228952', 'name': 'Acc. Dep-Leasehold Improvements'},
            'Hotels': {'id': '264337', 'name': 'Elon Baba'},
            'Trains': {'id': '228955', 'name': 'Sales - Merchandise'},
            'Flights': {'id': '228953', 'name': 'Customer Deposits'}
        }
    )
    
    mock_platform = MagicMock()
    mock_platform.v1.admin.categories.list.return_value = {'count': 1, 'data': [{'id': 'cat1'}]}
    mock_platform.v1.spender.expenses.post.return_value = {'data': {'id': 'exp1'}}
    mock_platform.v1.spender.files.create_file.return_value = {'data': {'id': 'file123'}}
    mock_platform.v1.spender.files.generate_file_urls.return_value = {'data': {'upload_url': 'http://upload'}}
    mock_platform.v1.spender.expenses.attach_receipt.return_value = True
    
    # Use shared mocks for all operations
    mock_fyle_connection(mocker)
    mock_file_ops = mock_file_operations(mocker)
    mock_employee_ops = mock_employee_operations(mocker)
    
    create_expense_in_fyle_v2(org_with_credentials.id, invoice, [invoice_lineitem])
    imported_expense = ImportedExpenseDetail.objects.filter(expense_id='exp1').first()
    assert imported_expense is not None


def test_create_expense_against_employee_multiple_case_1(mocker, org, invoice, advanced_settings, db):
    """
    Test create_expense_against_employee
    Case: MULTIPLE invoice lineitem structure
    """
    expense1 = InvoiceLineItem.objects.create(
        invoice=invoice, 
        total_amount=100.00,
        invoice_line_id='123',
        expense_date='2024-01-01',
        description='Test',
        trip_id='123',
        trip_name='Test Trip',
        service='flight',
        booker_email='test@test.com',
        traveller_email='test@test.com',
        credit_card_last_4_digits='1234'
    )
    expense2 = InvoiceLineItem.objects.create(
        invoice=invoice, 
        total_amount=200.00,
        invoice_line_id='124',
        expense_date='2024-01-01',
        description='Test',
        trip_id='123',
        trip_name='Test Trip',
        service='hotel',
        booker_email='test@test.com',
        traveller_email='test@test.com',
        credit_card_last_4_digits='1234'
    )
    
    # Use shared mock for invoice operations
    mock_invoice_ops = mock_invoice_operations(mocker)
    
    create_expense_against_employee(org.id, invoice, [expense1, expense2], 'BOOKER', advanced_settings)
    imported_expenses = ImportedExpenseDetail.objects.filter(org=org)
    assert imported_expenses.count() == 2


def test_create_expense_against_employee_single_case_1(mocker, org, invoice, advanced_settings, db):
    """
    Test create_expense_against_employee
    Case: SINGLE invoice lineitem structure
    """
    expense = InvoiceLineItem.objects.create(
        invoice=invoice, 
        total_amount=100.00,
        invoice_line_id='123',
        expense_date='2024-01-01',
        description='Test',
        trip_id='123',
        trip_name='Test Trip',
        service='flight',
        booker_email='test@test.com',
        traveller_email='test@test.com',
        credit_card_last_4_digits='1234'
    )
    
    # Use shared mock for invoice operations
    mock_invoice_ops = mock_invoice_operations(mocker)
    
    create_expense_against_employee(org.id, invoice, [expense], 'BOOKER', advanced_settings)
    imported_expense = ImportedExpenseDetail.objects.filter(org=org).first()
    assert imported_expense is not None


def test_create_expense_in_fyle_with_profile_mapping_case_1(mocker, org, invoice, invoice_lineitem, profile_mapping, advanced_settings, db):
    """
    Test create_expense_in_fyle
    Case: with profile mapping
    """
    # Use shared mock for expense operations
    mock_expense_ops = mock_expense_operations(mocker)
    
    create_expense_in_fyle(org.id, invoice, [invoice_lineitem])
    imported_expense = ImportedExpenseDetail.objects.filter(org=org).first()
    assert imported_expense is not None


def test_create_expense_in_fyle_without_profile_mapping_case_1(mocker, org, invoice, invoice_lineitem, db):
    """
    Test create_expense_in_fyle
    Case: without profile mapping
    """
    # Use shared mock for expense operations
    mock_expense_ops = mock_expense_operations(mocker)
    
    create_expense_in_fyle(org.id, invoice, [invoice_lineitem])
    imported_expense = ImportedExpenseDetail.objects.filter(org=org).first()
    assert imported_expense is not None


def test_add_travelperk_to_integrations_case_1(mocker, org, db):
    """
    Test add_travelperk_to_integrations
    Case: adds travelperk integration successfully
    """
    # Use shared mock for FYLE_CLIENT_ID
    mock_fyle_client_id(mocker)
    
    add_travelperk_to_integrations(org.id)
    integration = Integration.objects.filter(org_id=org.fyle_org_id, type='TRAVEL').first()
    assert integration is not None
    assert integration.is_active is True


def test_deactivate_travelperk_integration_case_1(mocker, org, db):
    """
    Test deactivate_travelperk_integration
    Case: deactivates travelperk integration successfully
    """
    # Create integration first
    Integration.objects.create(
        org_id=org.fyle_org_id,
        type='TRAVEL',
        is_active=True,
        org_name=org.name,
        tpa_id='test_id',
        tpa_name='Test Travelperk'
    )
    
    deactivate_travelperk_integration(org.id)
    integration = Integration.objects.get(org_id=org.fyle_org_id, type='TRAVEL')
    assert integration.is_active is False
    assert integration.disconnected_at is not None


def test_deactivate_travelperk_integration_org_not_found_case_1(mocker, db):
    """
    Test deactivate_travelperk_integration
    Case: org not found
    """
    deactivate_travelperk_integration(99999)
    # Function should return gracefully without raising exception
    integrations = Integration.objects.filter(type='TRAVEL')
    assert integrations.count() == 0


def test_deactivate_travelperk_integration_not_found_case_1(mocker, org, db):
    """
    Test deactivate_travelperk_integration
    Case: integration not found
    """
    deactivate_travelperk_integration(org.id)
    # Should not raise exception when integration doesn't exist
    integrations = Integration.objects.filter(org_id=org.fyle_org_id, type='TRAVEL')
    assert integrations.count() == 0
