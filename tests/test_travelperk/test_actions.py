import pytest

from apps.travelperk.actions import (
    construct_expense_payload,
    get_expense_purpose,
    create_invoice_lineitems,
    attach_reciept_to_expense,
    create_expense_in_fyle_v2,
    get_category_id,
    create_expense_against_employee,
    create_expense_in_fyle,
    add_travelperk_to_integrations,
    deactivate_travelperk_integration
)
from apps.travelperk.models import ImportedExpenseDetail, TravelperkProfileMapping, TravelperkAdvancedSetting
from apps.integrations.models import Integration
from tests.helper import dict_compare_keys
from .fixtures import (
    fixture,
    test_expense_purpose,
    test_category_id_flight,
    test_category_id_default,
    test_expense_id,
    test_file_id,
    test_integration_tpa_name,
    test_integration_tpa_id,
    test_integration_type,
    test_org_id_invalid,
    integration_test_data
)
from .mock_setup import (
    mock_construct_expense_payload_case_1, 
    mock_create_invoice_lineitems_case_1,
    mock_attach_reciept_to_expense_case_1,
    mock_test_create_expense_in_fyle_v2_case_1,
    mock_get_category_id_case_1,
    mock_create_expense_against_employee_case_1,
    mock_test_create_expense_in_fyle_case_1,
    mock_add_travelperk_to_integrations_case_1,
    mock_deactivate_travelperk_integration_case_1,
    mock_test_deactivate_travelperk_integration_case_2
)


@pytest.mark.shared_mocks(lambda mocker: mock_construct_expense_payload_case_1(mocker))
def test_construct_expense_payload_case_1(mock_dependencies, mocker, create_travelperk_full_setup):
    """
    Test construct_expense_payload action
    Case: Returns correct payload structure
    """
    setup = create_travelperk_full_setup
    invoice_lineitems = setup['invoice_lineitems']

    payload = None
    for expense in invoice_lineitems:
        payload = construct_expense_payload(setup['org'].id, expense, expense.total_amount, ['1321'], 'johndoe@gmail.com')

    assert dict_compare_keys(payload, fixture['payload']) == []


def test_get_expense_purpose_case_1(mock_dependencies, create_travelperk_full_setup):
    """
    Test get_expense_purpose action
    Case: Returns correct expense purpose
    """
    setup = create_travelperk_full_setup
    invoice_lineitems = setup['invoice_lineitems']

    for expense in invoice_lineitems:
        expense_purpose = get_expense_purpose(setup['org'].id, expense)
    
    assert expense_purpose == test_expense_purpose


@pytest.mark.shared_mocks(lambda mocker: mock_create_invoice_lineitems_case_1(mocker))
def test_create_invoice_lineitems_case_1(mock_dependencies, mocker, create_travelperk_full_setup):
    """
    Test create_invoice_lineitems action
    Case: Creates expense with correct data
    """
    setup = create_travelperk_full_setup
    invoice = setup['invoice']
    invoice_lineitems = setup['invoice_lineitems']

    expense = None
    for lineitem in invoice_lineitems:
        expense = lineitem

    imported_expense = create_invoice_lineitems(setup['org'].id, invoice, expense, 'BOOKER', 120)
    
    assert imported_expense.expense_id == '123'
    assert imported_expense.file_id == '123'


@pytest.mark.shared_mocks(lambda mocker: mock_attach_reciept_to_expense_case_1(mocker))
def test_attach_reciept_to_expense_case_1(mock_dependencies, mocker, create_travelperk_full_setup):
    """
    Test attach_reciept_to_expense action
    Case: Successfully attaches receipt to expense
    """
    setup = create_travelperk_full_setup
    invoice = setup['invoice']
    
    imported_expense = ImportedExpenseDetail.objects.create(
        expense_id=test_expense_id,
        org=setup['org'],
        is_reciept_attached=False,
        file_id=None
    )
    
    attach_reciept_to_expense(test_expense_id, invoice, imported_expense, mock_dependencies.platform_connection)
    
    assert imported_expense.is_reciept_attached is True
    assert imported_expense.file_id == test_file_id


@pytest.mark.shared_mocks(lambda mocker: mock_test_create_expense_in_fyle_v2_case_1(mocker))
def test_create_expense_in_fyle_v2_case_1(mock_dependencies, mocker, create_travelperk_full_setup):
    """
    Test create_expense_in_fyle_v2 action
    Case: Creates expense in Fyle with category mapping
    """
    setup = create_travelperk_full_setup
    invoice = setup['invoice']
    invoice_lineitems = setup['invoice_lineitems']
    
    create_expense_in_fyle_v2(setup['org'].id, invoice, invoice_lineitems)
    
    assert mock_dependencies.platform_connection.v1.spender.expenses.post.call_count == len(invoice_lineitems)
    assert invoice.exported_to_fyle is True


@pytest.mark.shared_mocks(lambda mocker: mock_get_category_id_case_1(mocker))
def test_get_category_id_case_1(mock_dependencies, create_travelperk_full_setup):
    """
    Test get_category_id action
    Case: Returns correct category ID for service
    """
    setup = create_travelperk_full_setup
    
    category_id = get_category_id(setup['org'].id, 'flight')
    
    assert category_id == test_category_id_flight


def test_get_category_id_case_2(mock_dependencies, create_travelperk_full_setup):
    """
    Test get_category_id action
    Case: Returns default category ID when service not found
    """
    setup = create_travelperk_full_setup
    
    category_id = get_category_id(setup['org'].id, 'unknown_service')
    
    assert category_id == test_category_id_default


@pytest.mark.shared_mocks(lambda mocker: mock_create_expense_against_employee_case_1(mocker))
def test_create_expense_against_employee_case_1(mock_dependencies, mocker, create_travelperk_full_setup):
    """
    Test create_expense_against_employee action
    Case: Creates multiple expenses for MULTIPLE structure
    """
    setup = create_travelperk_full_setup
    invoice = setup['invoice']
    invoice_lineitems = setup['invoice_lineitems']
    advanced_settings = setup['advanced_setting']
    
    create_expense_against_employee(setup['org'].id, invoice, invoice_lineitems, 'TRAVELLER', advanced_settings)
    
    mock_dependencies.create_invoice_lineitems.assert_called()


@pytest.mark.shared_mocks(lambda mocker: mock_test_create_expense_in_fyle_case_1(mocker))
def test_create_expense_in_fyle_case_1(mock_dependencies, mocker, create_travelperk_full_setup):
    """
    Test create_expense_in_fyle action
    Case: Creates expense with profile mapping and advanced settings
    """
    setup = create_travelperk_full_setup
    invoice = setup['invoice']
    invoice_lineitems = setup['invoice_lineitems']
    
    create_expense_in_fyle(setup['org'].id, invoice, invoice_lineitems)
    
    mock_dependencies.create_expense_against_employee.assert_called_once()


def test_create_expense_in_fyle_case_2(mock_dependencies, create_travelperk_full_setup):
    """
    Test create_expense_in_fyle action
    Case: Falls back to v2 when no profile mapping or advanced settings
    """
    setup = create_travelperk_full_setup
    invoice = setup['invoice']
    invoice_lineitems = setup['invoice_lineitems']
    
    TravelperkProfileMapping.objects.filter(org=setup['org']).delete()
    TravelperkAdvancedSetting.objects.filter(org=setup['org']).delete()
    
    with pytest.raises(Exception):
        create_expense_in_fyle(setup['org'].id, invoice, invoice_lineitems)


@pytest.mark.shared_mocks(lambda mocker: mock_add_travelperk_to_integrations_case_1(mocker))
def test_add_travelperk_to_integrations_case_1(mock_dependencies, create_travelperk_full_setup):
    """
    Test add_travelperk_to_integrations action
    Case: Successfully adds TravelPerk integration
    """
    setup = create_travelperk_full_setup
    
    add_travelperk_to_integrations(setup['org'].id)
    
    integration = Integration.objects.filter(
        org_id=setup['org'].fyle_org_id,
        type=test_integration_type
    ).first()
    
    assert integration is not None
    assert integration.is_active is True
    assert integration.tpa_name == test_integration_tpa_name


@pytest.mark.shared_mocks(lambda mocker: mock_deactivate_travelperk_integration_case_1(mocker))
def test_deactivate_travelperk_integration_case_1(mock_dependencies, create_travelperk_full_setup):
    """
    Test deactivate_travelperk_integration action
    Case: Successfully deactivates TravelPerk integration
    """
    setup = create_travelperk_full_setup
    
    integration = Integration.objects.create(
        org_id=setup['org'].fyle_org_id,
        type=test_integration_type,
        is_active=True,
        org_name=setup['org'].name,
        tpa_id=test_integration_tpa_id,
        tpa_name=test_integration_tpa_name
    )
    
    deactivate_travelperk_integration(setup['org'].id)
    
    integration.refresh_from_db()
    assert integration.is_active is False
    assert integration.disconnected_at is not None


@pytest.mark.shared_mocks(lambda mocker: mock_test_deactivate_travelperk_integration_case_2(mocker))
def test_deactivate_travelperk_integration_case_2(mock_dependencies):
    """
    Test deactivate_travelperk_integration action
    Case: Handles non-existent org gracefully
    """
    with pytest.raises(Exception, match='Org not found'):
        deactivate_travelperk_integration(test_org_id_invalid)
