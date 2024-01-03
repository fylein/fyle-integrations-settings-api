import requests
from datetime import datetime, timezone
import logging
from fyle.platform import Platform

from workato import Workato

from apps.travelperk.models import Invoice, InvoiceLineItem, TravelPerk, ImportedExpenseDetail
from apps.orgs.models import Org
from apps.orgs.utils import create_fyle_connection
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
        logger.info(f'Successfully downloaded the file to {local_filename}')
    else:
        # Print an error message if the file download fails
        logger.info(f'Failed to download the file. Status code: {response.status_code}')


def upload_to_s3_presigned_url(file_path, presigned_url):
    # Open the local file in binary read mode
    with open(file_path, 'rb') as file:
        headers = {
            'Content-Type': 'application/pdf'
        }

        # Send a PUT request to the S3 pre-signed URL with the file data
        response = requests.put(presigned_url, data=file, headers=headers)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Print a success message if the file is uploaded successfully
            logger.info(f'Successfully uploaded {file_path} to S3.')
        else:
            # Print an error message if the file upload fails
            logger.info(f'Failed to upload {file_path} to S3. Status code: {response.status_code}')


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
    download_path = 'tmp/{}-invoice.pdf'.format(expense_id)

    download_file(invoice.pdf, download_path)
    upload_to_s3_presigned_url(download_path, generate_url['data']['upload_url'])

    attached_reciept = platform_connection.v1beta.spender.expenses.attach_receipt({'data': {'id': expense_id, 'file_id': file['data']['id']}})

    if attached_reciept:
        imported_expense.file_id = file['data']['id']
        imported_expense.is_reciept_attached = True
        imported_expense.save()


def create_expense_in_fyle(org_id: str, invoice: Invoice, invoice_lineitems: InvoiceLineItem):
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

        category_name = CATEGORY_MAP[expense.service]
        platform_connection = create_fyle_connection(org.id)

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
