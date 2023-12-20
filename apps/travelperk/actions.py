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
