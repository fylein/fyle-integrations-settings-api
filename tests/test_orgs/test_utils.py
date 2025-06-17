import pytest
from apps.orgs.utils import create_fyle_connection, import_categories
from apps.orgs.models import Org, FyleCredential

@pytest.mark.django_db
def test_create_fyle_connection_success(settings, mocker):
    org = Org.objects.create(name='Test Org', fyle_org_id='org123', cluster_domain='https://test.com')
    FyleCredential.objects.create(org=org, refresh_token='token123')
    settings.FYLE_CLIENT_ID = 'id'
    settings.FYLE_CLIENT_SECRET = 'secret'
    settings.FYLE_TOKEN_URI = 'https://token.url'

    mock_platform = mocker.patch('apps.orgs.utils.Platform')
    create_fyle_connection(org.id)
    mock_platform.assert_called_once()

@pytest.mark.django_db
def test_import_categories_calls_sync(mocker):
    org = Org.objects.create(name='Test Org', fyle_org_id='org123', cluster_domain='https://test.com')
    FyleCredential.objects.create(org=org, refresh_token='token123')
    mock_connector = mocker.patch('apps.orgs.utils.PlatformConnector')
    mock_connector.return_value.sync_categories.return_value = ['cat1', 'cat2']
    result = import_categories(org.id)
    assert result == ['cat1', 'cat2']
