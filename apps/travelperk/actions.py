import requests
from datetime import datetime, timezone
import logging
from io import BytesIO
from fyle.platform import Platform


from apps.travelperk.models import Invoice, InvoiceLineItem, ImportedExpenseDetail
from apps.orgs.models import Org
from apps.orgs.utils import create_fyle_connection


CATEGORY_MAP = {
    'flight': 'Airlines',
    'car': 'Taxi',
    'train': 'Train',
    'hotel': 'Lodging',
    'pro_v2': 'Travelperk Charges'
}

logger = logging.getLogger(__name__)
logger.level = logging.INFO


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
