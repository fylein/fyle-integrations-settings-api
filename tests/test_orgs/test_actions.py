import pytest
from apps.orgs.actions import get_admin_employees
from apps.orgs.models import Org
from fyle_rest_auth.models import AuthToken

@pytest.mark.django_db
def test_get_admin_employees_success(mocker, django_user_model):
    org = Org.objects.create(name='Test Org', fyle_org_id='org123', cluster_domain='https://test.com')
    user = django_user_model.objects.create(user_id='user123', email='test@example.com')
    org.user.add(user)
    AuthToken.objects.create(user=user, refresh_token='token123')

    # Deep mock for the full attribute chain
    mock_employees = mocker.MagicMock()
    mock_employees.list_all.return_value = [
        {'data': [{'user': {'email': 'admin@example.com', 'full_name': 'Admin User'}}]}
    ]
    mock_admin = mocker.MagicMock(employees=mock_employees)
    mock_v1 = mocker.MagicMock(admin=mock_admin)
    mock_connection = mocker.MagicMock(v1=mock_v1)
    mock_platform = mocker.MagicMock(connection=mock_connection)
    mocker.patch('apps.orgs.actions.PlatformConnector', return_value=mock_platform)

    result = get_admin_employees(org.id, user.user_id)
    assert result == [{'email': 'admin@example.com', 'name': 'Admin User'}]

@pytest.mark.django_db
def test_get_admin_employees_org_not_found():
    with pytest.raises(Org.DoesNotExist):
        get_admin_employees(999, 'user123')
