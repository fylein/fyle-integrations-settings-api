import os
from unittest import mock
from datetime import datetime, timezone
import pytest
from fyle_rest_auth.models import User, AuthToken
from rest_framework.test import APIClient
from admin_settings import settings

from tests.fixture import fixture
from apps.orgs.models import Org, FyleCredential
from workato import Workato
from tests.test_workato.common.utils import get_mock_workato
from apps.gusto.models import Gusto, GustoConfiguration

def pytest_configure():
    os.system('sh ./tests/sql_fixtures/reset_db_fixtures/reset_db.sh')


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(scope='module')
def workato():
    connection = Workato()

    return connection

@pytest.fixture
def mock_workato():
    return get_mock_workato()

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

    def unpatch():
        patched_1.__exit__(None, None, None)
        patched_2.__exit__(None, None, None)
        patched_3.__exit__(None, None, None)
        patched_4.__exit__(None, None, None)
        patched_5.__exit__(None, None, None)
        patched_6.__exit__(None, None, None)

    request.addfinalizer(unpatch)


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
def gusto_environment():
    gusto = Gusto.objects.create(org = Org.objects.all().first(),
                         folder_id = "dummy",
                         package_id = "dummy"
                         )
    gusto_conf = GustoConfiguration.objects.create(
        org = Org.objects.all().first()
    )
    