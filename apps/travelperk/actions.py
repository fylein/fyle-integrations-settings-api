from datetime import datetime, timezone
import logging
import logging
from django.conf import settings
import requests
from datetime import datetime, timezone

from fyle.platform import Platform

from apps.integrations.models import Integration
from apps.orgs.exceptions import handle_fyle_exceptions
from apps.travelperk.models import (
    Invoice,
    InvoiceLineItem,
    ImportedExpenseDetail,
    TravelperkProfileMapping,
    TravelperkAdvancedSetting
)
from apps.orgs.utils import create_fyle_connection
from apps.orgs.models import Org
from apps.travelperk.helpers import (
    download_file,
    upload_to_s3_presigned_url,
    get_employee_email,
    get_email_from_credit_card_and_match_transaction,
    construct_file_ids
)


ROLE_EMAIL_MAPPING = {
    'TRAVELLER': 'traveller_email',
    'BOOKER': 'booker_email'
}


CATEGORY_MAP = {
    'flight': 'Airlines',
    'car': 'Taxi',
    'train': 'Train',
    'hotel': 'Lodging',
    'pro_v2': 'Travelperk Charges'
}

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def attach_reciept_to_expense(expense_id: str, invoice: Invoice, imported_expense: ImportedExpenseDetail, platform_connection: Platform):
    """
    Function to attach receipt to expense
    """

    file_payload = {
        'data': {
            'name': 'invoice.pdf',
            "type": "RECEIPT"
        }
    }

    file = platform_connection.v1beta.spender.files.create_file(file_payload)
    generate_url = platform_connection.v1beta.spender.files.generate_file_urls({'data': {'id': file['data']['id']}})

    file_content = download_file(invoice.pdf)
    upload_to_s3_presigned_url(file_content, generate_url['data']['upload_url'])

    attached_reciept = platform_connection.v1beta.spender.expenses.attach_receipt({'data': {'id': expense_id, 'file_id': file['data']['id']}})

    if attached_reciept:
        imported_expense.file_id = file['data']['id']
        imported_expense.is_reciept_attached = True
        imported_expense.save()


def create_expense_in_fyle_v2(org_id: str, invoice: Invoice, invoice_lineitems: InvoiceLineItem):
    """
    Create expense in Fyle
    """
    org = Org.objects.get(id=org_id)

    for expense in invoice_lineitems:
        payload = {
            'data': {
                'currency': invoice.currency,
                'purpose': expense.description,
                'merchant': expense.vendor['name'] if expense.vendor else '',
                'claim_amount': expense.total_amount,
                'spent_at': str(datetime.strptime(expense.expense_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)),
                'source': 'CORPORATE_CARD',
            }
        }

        platform_connection = create_fyle_connection(org.id)
        if expense.service in CATEGORY_MAP:
            category_name = CATEGORY_MAP[expense.service]

            query_params = {
                'limit': 1,
                'offset': 0,
                'order': "updated_at.asc",
                'system_category': "eq.{}".format(category_name),
                'is_enabled': "eq.True"
            }

            category = platform_connection.v1beta.admin.categories.list(query_params=query_params)

            if category['count'] > 0:
                payload['data']['category_id'] = category['data'][0]['id']

            expense = platform_connection.v1beta.spender.expenses.post(payload)

            if expense:
                imported_expense, _ = ImportedExpenseDetail.objects.update_or_create(
                    expense_id=expense['data']['id'],
                    org_id=org_id
                )
                attach_reciept_to_expense(expense['data']['id'], invoice, imported_expense, platform_connection)
                invoice.exported_to_fyle = True
                invoice.save()


def get_category_id(org_id:str, service: str):
    """
    get category id for the expense.
    """
    advance_settings = TravelperkAdvancedSetting.objects.filter(org_id=org_id).first()

    service  = '{}s'.format(service.capitalize())
    if service in advance_settings.category_mappings and advance_settings.category_mappings[service]:
        return advance_settings.category_mappings[service]['id']
    else:
        return advance_settings.default_category_id


def get_expense_purpose(org_id, lineitem) -> str:
    """
    purpose for expense in fyle
    """

    advanced_settings = TravelperkAdvancedSetting.objects.filter(org_id=org_id).first()
    memo_structure = advanced_settings.description_structure

    details = {
        'trip_id': str(lineitem.trip_id) if lineitem.trip_id else '',
        'trip_name': '{0}'.format(lineitem.trip_name) if lineitem.trip_name else '',
        'traveler_name': '{0}'.format(lineitem.traveller_name) if lineitem.traveller_name else '',
        'booker_name': '{0}'.format(lineitem.booker_name) if lineitem.booker_name else '',
        'merchant_name': '{0}'.format(lineitem.vendor['name']) if lineitem.vendor else '',
    }

    purpose = ''

    for id, field in enumerate(memo_structure):
        if field in details:
            purpose += details[field]
            if id + 1 != len(memo_structure):
                if details[field]:
                    purpose = '{0} - '.format(purpose)

    purpose = purpose.replace('<', '')
    purpose = purpose.replace('>', '')

    return purpose.rstrip(' - ')


def construct_expense_payload(org_id: str, expense: dict, amount: int, file_ids: list, employee_email: str):
    """
    Construct a payload for creating an expense.

    Parameters:
        user_role (str): Role of the user (e.g., 'TRAVELLER', 'BOOKER').
        expense (dict): Expense details.
        amount (int): Amount of the expense.
        employee_email (str): Employee's email address.

    Returns:
        dict: Expense payload.
    """

    purpose = get_expense_purpose(org_id, expense)
    category_id = get_category_id(org_id, expense.service.lower())

    payload = {
        'data': {
            'source': 'CORPORATE_CARD',
            'spent_at': str(datetime.strptime(expense.expense_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)),
            'purpose': purpose,
            'merchant': 'Travelperk',
            'category_id': category_id,
            'file_ids': file_ids
        }
    }

    if employee_email:
        payload['data']['admin_amount'] = amount
        payload['data']['assignee_user_email'] = employee_email
    else:
        payload['data']['claim_amount'] = amount

    return payload


@handle_fyle_exceptions(task_name='create expense in fyle')
def create_invoice_lineitems(org_id, invoice, expense, user_role, amount):
    """
    Function to create a single or multiple line expenses based on the user role.

    Parameters:
        org_id (str): Organization ID.
        expense (object): Expense object.
        user_role (str): Role of the user (e.g., 'TRAVELLER', 'BOOKER').
        amount (int): Amount of the expense.

    Returns:
        object: Created expense object.
    """

    # Establish a connection to the Fyle platform
    platform_connection = create_fyle_connection(org_id)
    matched_transaction = []

    # Determine the employee's email based on the user role
    if user_role in ['TRAVELLER', 'BOOKER']:
        travelperk_employee = getattr(expense, ROLE_EMAIL_MAPPING.get(user_role, None))
        employee_email = get_employee_email(platform_connection, travelperk_employee)
    else:
        employee_email, matched_transaction = get_email_from_credit_card_and_match_transaction(platform_connection, expense, amount)

    file_ids = construct_file_ids(platform_connection, invoice.pdf)
    payload = construct_expense_payload(org_id, expense, amount, file_ids, employee_email)

    if not matched_transaction:
        # Create the payload for the expense
        logger.info('expense created in fyle with org_id: {} and payload {}'.format(org_id, payload))

        if employee_email:
            created_expense = platform_connection.v1beta.admin.expenses.post(payload)
        else:
            created_expense = platform_connection.v1beta.spender.expenses.post(payload)

    else:
        payload['data']['id'] = matched_transaction[0]['matched_expense_ids'][0]
        created_expense = platform_connection.v1beta.admin.expenses.post(payload)

    imported_expense, _ = ImportedExpenseDetail.objects.update_or_create(
        expense_id=created_expense['data']['id'],
        is_reciept_attached=True,
        file_id=file_ids[0],
        org_id=org_id
    )

    return imported_expense


def create_expense_against_employee(org_id, invoice, invoice_lineitems, user_role, advanced_settings):
    """
    Function to create expenses against an employee based on the invoice line item structure.

    Parameters:
        org_id (str): Organization ID.
        invoice_lineitems (list): List of expense objects.
        user_role (str): Role of the user (e.g., 'TRAVELLER', 'BOOKER').
        advanced_settings (object): Advanced settings object.

    Returns:
        object: Created expense object.
    """

    # Check if the invoice line item structure is 'MULTIPLE'
    if advanced_settings.invoice_lineitem_structure == 'MULTIPLE':
        for expense in invoice_lineitems:
            created_expense = create_invoice_lineitems(org_id, invoice, expense, user_role, expense.total_amount)

    else:
        # Calculate the total amount for multiple line items
        total_amount = sum([float(expense.total_amount) for expense in invoice_lineitems])

        # Use the first expense as a representative for creating the expense against an employee
        expense = invoice_lineitems[0]

        # Create the expense against the employee with the total amount
        created_expense = create_invoice_lineitems(org_id, invoice, expense, user_role, total_amount)

    return created_expense


def create_expense_in_fyle(org_id: str, invoice: Invoice, invoice_lineitems: InvoiceLineItem):
    """
    Create expense in Fyle
    """
    profile_mapping = TravelperkProfileMapping.objects.filter(org_id=org_id, profile_name=invoice.profile_name).first()
    advanced_settings = TravelperkAdvancedSetting.objects.filter(org_id=org_id).first()
    if profile_mapping and advanced_settings:
        create_expense_against_employee(org_id, invoice, invoice_lineitems, profile_mapping.user_role, advanced_settings)
    else:
        create_expense_in_fyle_v2(org_id, invoice, invoice_lineitems)

def add_travelperk_to_integrations(org_id):
    org = Org.objects.get(id=org_id)
    logger.info(f'New integration record: Fyle TravelPerk Integration (TRAVEL) | {org.fyle_org_id = } | {org.name = }')

    Integration.objects.update_or_create(
        org_id=org.fyle_org_id,
        type='TRAVEL',
        defaults={
            'is_active': True,
            'org_name': org.name,
            'tpa_id': settings.FYLE_CLIENT_ID,
            'tpa_name': 'Fyle TravelPerk Integration'
        }
    )

def deactivate_travelperk_integration(org_id):
    """
    Deactivate the integration for the given org_id
    """
    try:
        org = Org.objects.get(id=org_id)
    except Org.DoesNotExist:
        logger.error(f'Org with id {org_id} not found')

    integration = Integration.objects.filter(org_id=org.fyle_org_id, type='TRAVEL').first()
    if integration:
        integration.is_active=False
        integration.disconnected_at=datetime.now()
        integration.save()
        logger.info(f'Deactivated integration: Fyle TravelPerk Integration (TRAVEL) | {org.fyle_org_id = } | {org.name = }')
    else:
        logger.error(f'Integration not found: Fyle TravelPerk Integration (TRAVEL) | {org.fyle_org_id = } | {org.name = }')
