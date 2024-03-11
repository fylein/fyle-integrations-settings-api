import json
import logging
import requests
from datetime import datetime, timezone

from django.conf import settings
from io import BytesIO

from apps.travelperk.models import TravelperkCredential
from apps.orgs.models import Org


logger = logging.getLogger(__name__)
logger.level = logging.INFO


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


def download_file(remote_url):
    # Send a GET request to the remote URL with streaming enabled
    response = requests.get(remote_url, stream=True)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        logger.info(f'Successfully downloaded the file. Status code: {response.status_code}')
        return BytesIO(response.content)
    else:
        # Print an error message if the file download fails
        logger.info(f'Failed to download the file. Status code: {response.status_code}')


def upload_to_s3_presigned_url(file_content, presigned_url):
    # Open the local file in binary read mode
    headers = {
        'Content-Type': 'application/pdf'
    }

    # Send a PUT request to the S3 pre-signed URL with the file data
    response = requests.put(presigned_url, data=file_content, headers=headers)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Print a success message if the file is uploaded successfully
        logger.info(f'Successfully uploaded to S3.')
    else:
        # Print an error message if the file upload fails
        logger.info(f'Failed to upload to S3. Status code: {response.status_code}')


def get_employee_email(platform_connection, employee_email):
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

    employee = platform_connection.v1beta.admin.employees.list(query_params)['data']

    return employee[0]['user']['email'] if employee else None


def check_for_transaction_in_fyle(platform_connection, expense, corporate_card_id, amount):
    """
    Check for Duplicate Transaction in Fyle

    Args:
    - platform_connection: Fyle platform connection object.
    - expense: Expense object containing details of the transaction.
    - corporate_card_id: ID of the corporate card used for the transaction.

    Returns:
    - corporate card transaction
    """

    # Prepare query parameters
    query_params = {
        'order': 'updated_at.asc',
        'corporate_card_id': f'eq.{corporate_card_id}',
        'amount': f'eq.{amount}',
        'spent_at': f'eq.{str(datetime.strptime(expense.expense_date, "%Y-%m-%d").replace(tzinfo=timezone.utc))}',
        'offset': 0,
        'limit': 1
    }

    # Fetch expense details from Fyle
    expense_details = platform_connection.v1beta.admin.corporate_card_transactions.list(query_params)['data']

    # Return expense details from Fyle
    return expense_details


def get_email_from_credit_card_and_match_transaction(platform_connection, expense, amount):
    """
    Get an email associated with a credit card based on its last 4 digits.

    Parameters:
        platform_connection: Fyle platform connection object.
        expense: Expense object containing credit card details.

    Returns:
        Tuple: (User's email associated with the credit card or None if not found,
                A boolean indicating whether a matched transaction is found or not)
    """
    # Query corporate cards based on last 4 digits of the credit card
    query_params = {
        'order': 'updated_at.asc',
        'card_number': f'ilike.%{expense.credit_card_last_4_digits}',
        'offset': 0,
        'limit': 1
    }

    credit_card_details = platform_connection.v1beta.admin.corporate_cards.list(query_params)['data']
    # Retrieve user ID and corporate credit card ID
    user_id = credit_card_details[0]['user_id'] if credit_card_details else None
    corporate_credit_card_id = credit_card_details[0]['id'] if credit_card_details else None

    # Check for matched transaction
    matched_transaction = check_for_transaction_in_fyle(platform_connection, expense, corporate_credit_card_id, amount)
    logger.info('matched transaction found for this expense with card digit: {}'.format(expense.credit_card_last_4_digits))

    # If user ID is found and no matched transaction is found
    if user_id and not matched_transaction_found:
        # Query employee details based on user ID
        query_params = {
            'user_id': f'eq.{user_id}',
            'order': "updated_at.asc",
            'offset': 0,
            'limit': 1
        }

        employee = platform_connection.v1beta.admin.employees.list(query_params)['data']

        # Return user's email and matched transaction status
        return employee[0]['user']['email'], matched_transaction_found

    # Return None and matched transaction status if user ID is not found or a matched transaction is found
    return None, matched_transaction_found


def construct_file_ids(platform_connection, url):
    """
    Construct File ids for reciepts
    """

    file_payload = {
        'data': {
            'name': 'invoice.pdf',
            "type": "RECEIPT"
        }
    }

    file = platform_connection.v1beta.spender.files.create_file(file_payload)
    generate_url = platform_connection.v1beta.spender.files.generate_file_urls({'data': {'id': file['data']['id']}})

    file_content = download_file(url)
    upload_to_s3_presigned_url(file_content, generate_url['data']['upload_url'])

    return [file['data']['id']]
