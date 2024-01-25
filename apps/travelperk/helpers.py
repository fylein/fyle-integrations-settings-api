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


def get_refresh_token_using_auth_code(code: str, org_id: str):

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


def construct_expense_payload(user_role: str, expense: dict, employee_email: str = None):
    payload = {
        'data': {
            'source': 'CORPORATE_CARD',
            'spent_at': str(datetime.strptime(expense.expense_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)),
            'purpose': expense.description,
            'merchant': expense.vendor['name'] if expense.vendor else '',
            'category_id': 142039
        }
    }

    if user_role in ['TRAVELLER', 'BOOKER', 'CARD_HOLDER'] and employee_email:
        payload['data']['assignee_user_email'] = employee_email
        payload['data']['admin_amount'] = expense.total_amount
    else:
        payload['data']['claim_amount'] = expense.total_amount

    return payload


def create_expense_against_employee(org_id, invoice_lineitems, user_role):

    role_email_mapping = {
        'TRAVELLER': 'traveller_email', 
        'BOOKER': 'booker_email'
    }

    for expense in invoice_lineitems:
        if user_role in ['TRAVELLER', 'BOOKER']:
            travelperk_employee = getattr(expense, role_email_mapping.get(user_role, None))
            employee_email = get_employee_email(org_id, travelperk_employee)
        else:
            employee_email = get_email_from_credit_card(org_id, expense.credit_card_last_4_digits)

        payload = construct_expense_payload(user_role, expense, employee_email)
        platform_connection = create_fyle_connection(org_id)

        if employee_email:
            expense = platform_connection.v1beta.admin.expenses.post(payload)
        else:
            expense = platform_connection.v1beta.spender.expenses.post(payload)

        return expense
