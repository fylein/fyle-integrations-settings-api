from unittest import mock
from datetime import datetime, timezone
import pytest
from fyle_rest_auth.models import User, AuthToken
from rest_framework.test import APIClient
from admin_settings import settings

from tests.fixture import fixture
from apps.orgs.models import Org, FyleCredential
from apps.travelperk.models import TravelPerk, TravelperkProfileMapping, TravelperkAdvancedSetting, TravelperkCredential
from apps.bamboohr.models import BambooHr, BambooHrConfiguration

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
        'fyle.platform.apis.v1beta.spender.MyProfile.get',
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
def access_token():
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
def get_org_id():
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
def get_bamboohr_id(mocker, get_org_id):
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
def get_travelperk(get_org_id):
    travelperk = TravelPerk.objects.create(
        org = Org.objects.get(id = get_org_id),
        folder_id = "dummy",
        package_id = "dummy",
        is_travelperk_connected = True
    )

    return travelperk.id

@pytest.fixture()
def get_travelperk_id(get_org_id):
    travelperk = TravelPerk.objects.create(
        org = Org.objects.get(id = get_org_id),
        folder_id = "dummy",
        package_id = "dummy",
        is_travelperk_connected = True
    )

    return travelperk.id

@pytest.fixture()
def get_profile_mappings(get_org_id):
    mappings = TravelperkProfileMapping.objects.create(
        org=Org.objects.get(id=get_org_id),
        profile_name='Dummy Profile',
        user_role='BOOKER',
        is_import_enabled=False,
        source_id='1234',
        currency='USD'
    )

@pytest.fixture()
def get_advanced_settings(get_org_id):
    advanced_settings = TravelperkAdvancedSetting.objects.create(
        org=Org.objects.get(id=get_org_id),
        default_employee_name='dummy@gmail.com',
        default_employee_id='1234',
        invoice_lineitem_structure='MULTIPLE',
    )

@pytest.fixture()
def add_travelperk_cred(get_org_id):
    travelperk_cred = TravelperkCredential.objects.create(
        org=Org.objects.get(id=get_org_id),
        refresh_token='12312rwer'
    )
