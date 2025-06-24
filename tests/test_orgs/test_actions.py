import pytest
from apps.orgs.actions import get_admin_employees
from apps.orgs.models import Org
from tests.test_orgs.mock_setup import mock_platform_connector_shared_mock

@pytest.mark.shared_mocks(lambda mocker: mock_platform_connector_shared_mock(mocker))
def test_get_admin_employees_success(mock_dependencies, add_org, db):
    """
    Test get_admin_employees with valid org
    """
    # Create a user for the org
    from fyle_rest_auth.models import User, AuthToken
    user = User.objects.create(
        user_id='user123',
        email='test@example.com',
        full_name='Test User'
    )
    add_org.user.add(user)
    AuthToken.objects.create(user=user, refresh_token='token123')

    employees = get_admin_employees(add_org.id, user.user_id)
    assert employees is not None
    assert len(employees) > 0

@pytest.mark.shared_mocks(lambda mocker: mock_platform_connector_shared_mock(mocker))
def test_get_admin_employees_org_not_found(mock_dependencies, db):
    """
    Test get_admin_employees with non-existent org
    """
    with pytest.raises(Org.DoesNotExist):
        get_admin_employees(99999, 'user123')
