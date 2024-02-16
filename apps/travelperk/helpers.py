import json
import logging
import requests

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


def get_email_from_credit_card(platform_connection, credit_card_last_4_digits):
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
