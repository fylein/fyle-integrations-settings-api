import os
from unittest import mock
from datetime import datetime, timezone
import pytest
from fyle_rest_auth.models import User, AuthToken
from rest_framework.test import APIClient

from tests.fixture import fixture


def pytest_configure():
    os.system('sh ./tests/sql_fixtures/reset_db_fixtures/reset_db.sh')


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


    patched_4 = mock.patch(
        'fyle.platform.apis.v1beta.spender.MyProfile.get',
        return_value=fixture['my_profile']
    )
    patched_4.__enter__()

    patched_6 = mock.patch(
        'fyle_rest_auth.helpers.get_fyle_admin',
        return_value=fixture['my_profile']
    )
    patched_6.__enter__()

    def unpatch():
        patched_1.__exit__(None, None, None)
        patched_2.__exit__(None, None, None)
        patched_4.__exit__(None, None, None)
        patched_6.__exit__(None, None, None)

    request.addfinalizer(unpatch)


@pytest.fixture()
def access_token():
    create_user_and_tokens()
    return 'abcd.efgh.jklm'


def create_user_and_tokens():
    user = create_user('ashwin.t@fyle.in', 'Joanna', 'usqywo0f3nBY')
    create_auth_token(user)

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
