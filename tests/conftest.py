from unittest import mock
from datetime import datetime, timezone
import pytest
from fyle_rest_auth.models import User, AuthToken
from rest_framework.test import APIClient
from admin_settings import settings
from unittest.mock import MagicMock
import uuid

from tests.fixture import fixture
from apps.orgs.models import (
    Org,
    FyleCredential
)
from apps.bamboohr.models import (
    BambooHr,
    BambooHrConfiguration
)
from apps.travelperk.models import (
    TravelPerk,
    TravelperkProfileMapping,
    TravelperkAdvancedSetting,
    TravelperkCredential,
    Invoice,
    InvoiceLineItem
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="session", autouse=True)
def default_session_fixture(request):
    patched_1 = mock.patch(
        'fyle_rest_auth.authentication.get_fyle_admin',
        return_value=fixture['my_profile']
    )
    patched_1.__enter__()

    patched_2 = mock.patch(
        'fyle.platform.internals.auth.Auth.update_access_token',
        return_value='abcd'
    )
    patched_2.__enter__()

    patched_3 = mock.patch(
        'apps.users.helpers.post_request',
        return_value={
            'access_token': 'abcd.efgh.jklm',
            'cluster_domain': 'https://lolo.fyle.tech'
        }
    )
    patched_3.__enter__()

    patched_4 = mock.patch(
        'fyle.platform.apis.v1.spender.MyProfile.get',
        return_value=fixture['my_profile']
    )
    patched_4.__enter__()

    patched_5 = mock.patch(
        'apps.users.helpers.get_cluster_domain',
        return_value='https://lolo.fyle.tech'
    )
    patched_5.__enter__()

    patched_6 = mock.patch(
        'fyle_rest_auth.helpers.get_fyle_admin',
        return_value=fixture['my_profile']
    )
    patched_6.__enter__()


@pytest.fixture()
def add_org(db):
    """
    Create a test organization with basic setup
    """
    org = Org.objects.create(
        name='Test Organization',
        fyle_org_id='orTest123',
        cluster_domain='https://test.fyle.tech'
    )
    return org


@pytest.fixture()
def add_org_with_credentials(db):
    """
    Create a test organization with FyleCredential
    """
    org = Org.objects.create(
        name='Test Organization',
        fyle_org_id='orTest123',
        cluster_domain='https://test.fyle.tech'
    )
    fyle_credential = FyleCredential.objects.create(
        org=org,
        refresh_token='test_refresh_token'
    )
    return org


@pytest.fixture()
def access_token(db):
    create_user_and_tokens()
    return 'abcd.efgh.jklm'


def create_user_and_tokens():
    user = create_user('ashwin.t@fyle.in', 'Joanna', 'usqywo0f3nBY')
    create_auth_token(user)


    org = Org.objects.create(
        name='Anagha Org', fyle_org_id='orHVw3ikkCxJ', cluster_domain='https://lolo.fyle.tech'
    )
    org.user.add(user)
    FyleCredential.objects.create(
        refresh_token=settings.FYLE_REFRESH_TOKEN,
        org=org,
    )

    user = create_user('ashwin.t+1@fyle.in', 'Joannaa', 'usqywo0f3nBZ')
    create_auth_token(user)


def create_user(email: str, name: str, user_id: str) -> User:
    return User.objects.create(
        password='', last_login=datetime.now(tz=timezone.utc), email=email,
        user_id=user_id, full_name=name, active='t', staff='f', admin='f'
    )


def create_auth_token(user: User):
    AuthToken.objects.create(
        refresh_token='refresh_token',
        user=user
    )

@pytest.fixture()
def get_org_id(db):
    # create an org
    org = Org.objects.create(
        name = 'Test org',
        fyle_org_id = 'orTwovfDpEYc',
        managed_user_id = '890744',
        cluster_domain='https://fake-cluster-domain.com',
    )
    # create fyle credentials for it
    fyle_creds = FyleCredential.objects.create(
        refresh_token = 'fake-refresh-token',
        org = org
    )
    return org.id


@pytest.fixture()
def get_bamboohr_id(mocker, get_org_id, db):
    bamboohr = BambooHr.objects.create(
        org = Org.objects.get(id = get_org_id),
        folder_id = "1234",
        package_id = "1234"
    )
    BambooHrConfiguration.objects.create(
        org = Org.objects.get(id = get_org_id)
    )
    return bamboohr.id


@pytest.fixture()
def get_travelperk(get_org_id, db):
    travelperk = TravelPerk.objects.create(
        org = Org.objects.get(id = get_org_id),
        folder_id = "dummy",
        package_id = "dummy",
        is_travelperk_connected = True
    )

    return travelperk

@pytest.fixture()
def get_travelperk_id(get_org_id, db):
    travelperk = TravelPerk.objects.create(
        org = Org.objects.get(id = get_org_id),
        folder_id = "dummy",
        package_id = "dummy",
        is_travelperk_connected = True
    )

    return travelperk.id

@pytest.fixture()
def get_profile_mappings(get_org_id, db):
    profile_mappings = TravelperkProfileMapping.objects.create(
        org=Org.objects.get(id=get_org_id),
        profile_name='Dummy Profile',
        user_role='BOOKER',
        is_import_enabled=False,
        source_id='1234',
        currency='USD'
    )

    return profile_mappings


@pytest.fixture()
def get_advanced_settings(get_org_id, db):
    advanced_settings = TravelperkAdvancedSetting.objects.create(
        org=Org.objects.get(id=get_org_id),
        default_employee_name='dummy@gmail.com',
        default_employee_id='1234',
        invoice_lineitem_structure='MULTIPLE',
        description_structure='{trip_id,trip_name,traveler_name,booker_name,merchant_name}'
    )

    return advanced_settings


@pytest.fixture()
def add_travelperk_cred(get_org_id, db):
    travelperk_cred = TravelperkCredential.objects.create(
        org=Org.objects.get(id=get_org_id),
        refresh_token='12312rwer'
    )

@pytest.fixture()
def add_invoice_and_invoice_lineitems(get_org_id, db):

    data = fixture['expense']
    invoice_lineitems_data = data['lines']

    # Create or update Invoice and related line items
    invoice = Invoice.create_or_update_invoices(data, get_org_id)
    invoice_lineitems = InvoiceLineItem.create_or_update_invoice_lineitems(invoice_lineitems_data, invoice)

    return invoice, invoice_lineitems


# Shared Mocks Support
@pytest.fixture()
def mock_dependencies(request, mocker):
    """
    Apply shared mocks to tests marked with @pytest.mark.shared_mocks
    """
    class MockContainer:
        pass

    mock_container = MockContainer()

    # Apply shared mocks from the decorator
    shared_mocks_marker = request.node.get_closest_marker("shared_mocks")
    if shared_mocks_marker:
        for mock_func in shared_mocks_marker.args:
            shared_mocks = mock_func(mocker)
            for key, value in shared_mocks.items():
                setattr(mock_container, key, value)

    return mock_container

@pytest.fixture()
def org(db):
    return Org.objects.create(name='Test Org', fyle_org_id=f'orTwovfDpEYc_{uuid.uuid4()}')

@pytest.fixture()
def org_with_credentials(db):
    org = Org.objects.create(name='Test Org', fyle_org_id=f'orTwovfDpEYc_{uuid.uuid4()}')
    FyleCredential.objects.create(org=org, refresh_token='dummy_refresh_token')
    return org

@pytest.fixture()
def invoice(org, db):
    return Invoice.objects.create(
        org=org,
        currency='USD',
        billing_information={'name': 'Test'},
        billing_period='instant',
        due_date='2024-01-01',
        from_date='2024-01-01',
        to_date='2024-01-01',
        issuing_date='2024-01-01',
        mode='direct',
        pdf='http://test.pdf',
        profile_id='123',
        profile_name='Test Profile',
        reference='Test Ref',
        serial_number='123',
        status='paid',
        taxes_summary={},
        total=100.00
    )

@pytest.fixture()
def invoice_lineitem(invoice, db):
    return InvoiceLineItem.objects.create(
        invoice=invoice,
        service='flight',
        description='Flight to West Lisaville',
        total_amount=100.00,
        expense_date='2024-04-12',
        invoice_line_id='10205',
        trip_id='10205',
        trip_name='Flight to West Lisaville',
        booker_email='nilesh.pant@fyle.in',
        traveller_email='nilesh.pant@fyle.in',
        credit_card_last_4_digits='1234',
        booker_name='Nilesh Pant',
        traveller_name='Nilesh Pant',
        vendor={'name': 'Vueling'}
    )

@pytest.fixture()
def advanced_settings(org, db):
    return TravelperkAdvancedSetting.objects.create(
        org=org,
        default_employee_name='ashwin.t@fyle.in',
        default_employee_id='usqywo0f3nBY',
        default_category_name='Acc. Dep-Leasehold Improvements',
        default_category_id='228952',
        invoice_lineitem_structure='MULTIPLE',
        description_structure=[
            'trip_id',
            'trip_name',
            'traveler_name',
            'booker_name',
            'merchant_name'
        ],
        category_mappings={
            'Cars': {'id': '228952', 'name': 'Acc. Dep-Leasehold Improvements'},
            'Hotels': {'id': '264337', 'name': 'Elon Baba'},
            'Trains': {'id': '228955', 'name': 'Sales - Merchandise'},
            'Flights': {'id': '228953', 'name': 'Customer Deposits'}
        }
    )

@pytest.fixture()
def profile_mapping(org, db):
    return TravelperkProfileMapping.objects.create(
        org=org,
        profile_name='Test Profile',
        user_role='BOOKER'
    )

@pytest.fixture()
def mock_expense():
    expense = MagicMock()
    expense.expense_date = '2024-01-01'
    expense.credit_card_last_4_digits = '1234'
    return expense

@pytest.fixture()
def mock_conn():
    return MagicMock()

@pytest.fixture()
def mock_settings(monkeypatch):
    from apps.travelperk import helpers
    monkeypatch.setattr(helpers, 'settings', MagicMock())
    helpers.settings.TRAVELPERK_TOKEN_URL = 'http://fake-url/token'
    helpers.settings.TRAVELPERK_CLIENT_ID = 'client_id'
    helpers.settings.TRAVELPERK_CLIENT_SECRET = 'client_secret'
    helpers.settings.TRAVELPERK_REDIRECT_URI = 'http://fake-url/redirect'
    return helpers.settings
