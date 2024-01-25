import requests
import logging
from io import BytesIO
from fyle.platform import Platform

from workato import Workato

from apps.orgs.models import Org
from apps.orgs.utils import create_fyle_connection
from apps.orgs.exceptions import handle_workato_exception
from apps.names import TRAVELPERK
from apps.travelperk.models import (
    Invoice, 
    InvoiceLineItem, 
    TravelPerk, 
    ImportedExpenseDetail,
    TravelperkProfileMapping
)
from .helpers import create_expense_against_employee, get_email_from_credit_card

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



def create_expense_in_fyle(org_id: str, invoice: Invoice, invoice_lineitems: InvoiceLineItem):
    """
    Create expense in Fyle
    """
    profile_mapping = TravelperkProfileMapping.objects.filter(org_id=org_id, profile_name=invoice.profile_name).first()
    platform_connection = create_fyle_connection(org_id)

    if profile_mapping and profile_mapping.is_import_enabled:
        expense = create_expense_against_employee(org_id, invoice_lineitems, profile_mapping.user_role)
        if expense:
            imported_expense, _ = ImportedExpenseDetail.objects.update_or_create(
                expense_id=expense['data']['id'],
                org_id=org_id
            )

            attach_reciept_to_expense(expense['data']['id'], invoice, imported_expense, platform_connection)
            invoice.exported_to_fyle = True
            invoice.save()
