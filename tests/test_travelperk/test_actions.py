import pytest

from apps.travelperk.actions import (
    construct_expense_payload,
    get_expense_purpose,
    create_invoice_lineitems
)
from tests.helper import dict_compare_keys
from .fixtures import fixture
from .mock_setup import mock_construct_expense_payload_case_1, mock_create_invoice_lineitems_case_1


@pytest.mark.shared_mocks(lambda mocker: mock_construct_expense_payload_case_1(mocker))
def test_construct_expense_payload_case_1(mock_dependencies, mocker, create_org, create_invoice_and_invoice_lineitems, create_travelperk_advanced_setting, db):
    """
    Test construct_expense_payload action
    Case: Returns correct payload structure
    """
    _, invoice_lineitems = create_invoice_and_invoice_lineitems

    payload = None
    for expense in invoice_lineitems:
        payload = construct_expense_payload(create_org.id, expense, expense.total_amount, ['1321'], 'johndoe@gmail.com')

    assert dict_compare_keys(payload, fixture['payload']) == []


def test_get_expense_purpose_case_1(mock_dependencies, create_org, create_invoice_and_invoice_lineitems, create_travelperk_advanced_setting, db):
    """
    Test get_expense_purpose action
    Case: Returns correct expense purpose
    """
    _, invoice_lineitems = create_invoice_and_invoice_lineitems

    for expense in invoice_lineitems:
        expense_purpose = get_expense_purpose(create_org.id, expense)
    
    assert expense_purpose == '10205 - Flight to West Lisaville, Apr 12 - Apr 13 - Nilesh Pant - Nilesh Pant - Vueling'


@pytest.mark.shared_mocks(lambda mocker: mock_create_invoice_lineitems_case_1(mocker))
def test_create_invoice_lineitems_case_1(mock_dependencies, mocker, create_org, create_invoice_and_invoice_lineitems, create_travelperk_profile_mapping, create_travelperk_advanced_setting, db):
    """
    Test create_invoice_lineitems action
    Case: Creates expense with correct data
    """
    invoice, invoice_lineitems = create_invoice_and_invoice_lineitems

    expense = None
    for lineitem in invoice_lineitems:
        expense = lineitem

    imported_expense = create_invoice_lineitems(create_org.id, invoice, expense, 'BOOKER', 120)
    
    assert imported_expense.expense_id == '123'
    assert imported_expense.file_id == '123'
