import requests
import logging
from django.conf import settings
from fyle.platform import Platform

from workato import Workato

from apps.travelperk.models import Invoice, InvoiceLineItem, TravelPerk
from apps.orgs.models import Org, FyleCredential
from apps.orgs.exceptions import handle_workato_exception
from apps.names import TRAVELPERK


CATEGORY_MAP = {
    'flight': 'Airlines',
    'car': 'Taxi',
    'train': 'Train',
    'hotel': 'Lodging',
    'pro_v2': 'Travelperk Charges'
}

logger = logging.getLogger(__name__)
logger.level = logging.INFO


@handle_workato_exception(task_name = 'Travelperk Connection')
def connect_travelperk(org_id):
    connector = Workato()
    org = Org.objects.get(id=org_id)
    travelperk = TravelPerk.objects.get(org_id=org.id)
    connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
    connection_id = next(connection for connection in connections if connection['name'] == TRAVELPERK['connection'])['id']

    travelperk.travelperk_connection_id = connection_id
    travelperk.save()
    return connection_id


def download_file(remote_url, local_filename):
    # Send a GET request to the remote URL with streaming enabled
    response = requests.get(remote_url, stream=True)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Open a local file in binary write mode
        with open(local_filename, 'wb') as file:
            # Iterate over the content in chunks and write to the local file
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        # Print a success message if the file is downloaded successfully
        logger.log(f'Successfully downloaded the file to {local_filename}')
    else:
        # Print an error message if the file download fails
        logger.log(f'Failed to download the file. Status code: {response.status_code}')


def upload_to_s3_presigned_url(file_path, presigned_url):
    # Open the local file in binary read mode
    with open(file_path, 'rb') as file:
        # Send a PUT request to the S3 pre-signed URL with the file data
        response = requests.put(presigned_url, data=file)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Print a success message if the file is uploaded successfully
            logger.log(f'Successfully uploaded {file_path} to S3.')
        else:
            # Print an error message if the file upload fails
            logger.log(f'Failed to upload {file_path} to S3. Status code: {response.status_code}')


def create_expense_in_fyle(org_id: str, invoice: Invoice, invoice_lineitem: InvoiceLineItem):
    """
    Create expense in Fyle
    """
    org = Org.objects.get(id=org_id)
    fyle_credentials = FyleCredential.objects.get(org=org)

    for expense in invoice_lineitem:
        payload = {
            'data': {
                'currency': invoice.currency,
                'purpose': expense.description,
                'merchant': expense.vendor,
                'claim_amount': expense.total_amount,
                'spent_at': '2023-06-01',
                'source': 'CORPORATE_CARD',
            }
        }

        category_name = CATEGORY_MAP[expense.service]

        server_url = '{}/platform/v1beta'.format(org.cluster_domain)
        platform_connection = Platform(
            server_url=server_url,
            token_url=settings.FYLE_TOKEN_URI,
            client_id=settings.FYLE_CLIENT_ID,
            client_secret=settings.FYLE_CLIENT_SECRET,
            refresh_token=fyle_credentials.refresh_token
        )

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
            invoice.exported_to_fyle = True
            invoice.save()
