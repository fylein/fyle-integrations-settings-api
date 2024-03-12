import pytest

from apps.travelperk.actions import (
    construct_expense_payload,
    get_expense_purpose,
    create_invoice_lineitems
)
from tests.helper import dict_compare_keys
from .fixtures import fixture


@pytest.mark.django_db(databases=['default'])
def test_construct_expense_payload(mocker, get_org_id, add_invoice_and_invoice_lineitems, get_advanced_settings):
    """
    test construct payload function
    """

    mocker.patch('apps.travelperk.actions.get_category_id', return_value='1234')

    _, invoice_lineitems = add_invoice_and_invoice_lineitems

    payload = None
    for expense in invoice_lineitems:
        payload = construct_expense_payload(get_org_id, expense, expense.total_amount)

    assert dict_compare_keys(payload, fixture['payload']) == []


@pytest.mark.django_db(databases=['default'])
def test_get_expense_purpose(get_org_id, add_invoice_and_invoice_lineitems, get_advanced_settings):
    """
    test get expense purpose
    """

    _, invoice_lineitems = add_invoice_and_invoice_lineitems

    for expense in invoice_lineitems:
        expense_purpose = get_expense_purpose(get_org_id, expense)
    
    assert expense_purpose == '10205 - Flight to West Lisaville, Apr 12 - Apr 13 - Nilesh Pant - Nilesh Pant - Vueling'


@pytest.mark.django_db(databases=['default'])
def test_create_invoice_lineitems(get_org_id, add_invoice_and_invoice_lineitems, get_profile_mappings, get_advanced_settings):
    
    profile_mappings = get_profile_mappings
    advanced_settings = get_advanced_settings
    invoice, invoice_lineitems = add_invoice_and_invoice_lineitems

    expense = None
    for lineitem in invoice_lineitems:
        expense = lineitem

    create_invoice_lineitems(get_org_id, invoice, expense, 'BOOKER', 120)