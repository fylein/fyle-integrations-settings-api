import json
import logging
import requests
from datetime import datetime, timezone
from django.conf import settings

from apps.travelperk.models import TravelperkCredential, TravelperkAdvancedSetting
from apps.orgs.models import Org
from apps.orgs.utils import create_fyle_connection

logger = logging.getLogger(__name__)
logger.level = logging.INFO

ROLE_EMAIL_MAPPING = {
    'TRAVELLER': 'traveller_email',
    'BOOKER': 'booker_email'
}

def get_refresh_token_using_auth_code(code: str, org_id: str):
    """
    Get a refresh token using the authorization code obtained during the OAuth 2.0 flow.

    Parameters:
        code (str): Authorization code.
        org_id (str): Organization ID.

    Returns:
        str: Refresh token.

    Raises:
        Exception: If the API response status code is not 200.
    """

    response = requests.post(
        url=settings.TRAVELPERK_TOKEN_URL,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': settings.TRAVELPERK_CLIENT_ID,
            'client_secret': settings.TRAVELPERK_CLIENT_SECRET,
            'redirect_uri': settings.TRAVELPERK_REDIRECT_URI
        }
    )

    api_response = json.loads(response.text)

    if response.status_code == 200:
        org = Org.objects.get(id=org_id)
        travelperk_credential, _ = TravelperkCredential.objects.update_or_create(
            org=org,
            defaults={
                'refresh_token': api_response['refresh_token'],
            }
        )

        return api_response['refresh_token']
    else:
        raise Exception(api_response)


def get_employee_email(org_id, employee_email):
    """
    Get an employee's email using their email address.

    Parameters:
        org_id (str): Organization ID.
        employee_email (str): Employee's email address.

    Returns:
        str: Employee's email or None if not found.
    """
    query_params = {
        'user->email': f'eq.{employee_email}',
        'order': "updated_at.asc",
        'offset': 0,
        'limit': 1
    }

    platform_connection = create_fyle_connection(org_id)
    employee = platform_connection.v1beta.admin.employees.list(query_params)['data']

    return employee[0]['user']['email'] if employee else None


def get_email_from_credit_card(org_id, credit_card_last_4_digits):
    """
    Get an email associated with a credit card based on its last 4 digits.

    Parameters:
        org_id (str): Organization ID.
        credit_card_last_4_digits (str): Last 4 digits of the credit card.

    Returns:
        str: User's email associated with the credit card or None if not found.
    """
    query_params = {
        'order': 'updated_at.asc',
        'card_number': f'ilike.%{credit_card_last_4_digits}',
        'offset': 0,
        'limit': 1
    }

    platform_connection = create_fyle_connection(org_id)
    credit_card_details = platform_connection.v1beta.admin.corporate_cards.list(query_params)['data']

    user_id = credit_card_details[0]['user_id'] if credit_card_details else None

    if user_id:
        query_params = {
            'user_id': f'eq.{user_id}',
            'order': "updated_at.asc",
            'offset': 0,
            'limit': 1
        }

        employee = platform_connection.v1beta.admin.employees.list(query_params)['data']
        return employee[0]['user']['email'] if employee else None

    return None


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
        'trip_id': lineitem.trip_id if lineitem.trip_id else '',
        'trip_name': '{0}'.format(lineitem.trip_name) if lineitem.trip_name else '',
        'traveller_name': '{0}'.format(lineitem.traveller_name) if lineitem.traveller_name else '',
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

    return purpose


def construct_expense_payload(org_id: str, user_role: str, expense: dict, amount: int, employee_email: str = None):
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
            'merchant': expense.vendor['name'] if expense.vendor else '',
            'category_id': category_id,
        }
    }

    if user_role in ['TRAVELLER', 'BOOKER', 'CARD_HOLDER'] and employee_email:
        payload['data']['assignee_user_email'] = employee_email
        payload['data']['admin_amount'] = amount
    else:
        payload['data']['claim_amount'] = amount

    return payload


def create_invoice_lineitems(org_id, expense, user_role, amount):
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

    # Determine the employee's email based on the user role
    if user_role in ['TRAVELLER', 'BOOKER']:
        travelperk_employee = getattr(expense, ROLE_EMAIL_MAPPING.get(user_role, None))
        employee_email = get_employee_email(org_id, travelperk_employee)
    else:
        employee_email = get_email_from_credit_card(org_id, expense.credit_card_last_4_digits)

    # Create the payload for the expense
    payload = construct_expense_payload(org_id, user_role, expense, amount, employee_email)

    # Establish a connection to the Fyle platform
    platform_connection = create_fyle_connection(org_id)

    # Post the expense to the appropriate endpoint based on the presence of an employee email
    if employee_email:
        expense = platform_connection.v1beta.admin.expenses.post(payload)
    else:
        expense = platform_connection.v1beta.spender.expenses.post(payload)

    return expense


def create_expense_against_employee(org_id, invoice_lineitems, user_role, advanced_settings):
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
            created_expense = create_invoice_lineitems(org_id, expense, user_role, expense.total_amount)

    else:
        # Calculate the total amount for multiple line items
        total_amount = sum([float(expense.total_amount) for expense in invoice_lineitems])

        # Use the first expense as a representative for creating the expense against an employee
        expense = invoice_lineitems[0]

        # Create the expense against the employee with the total amount
        created_expense = create_invoice_lineitems(org_id, expense, user_role, total_amount)

    return created_expense
