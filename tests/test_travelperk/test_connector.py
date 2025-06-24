import pytest
from apps.travelperk.connector import TravelperkConnector
from unittest.mock import MagicMock

@pytest.fixture
def mock_settings(monkeypatch):
    class DummySettings:
        TRAVELPERK_CLIENT_ID = 'client_id'
        TRAVELPERK_CLIENT_SECRET = 'client_secret'
        TRAVELPERK_ENVIRONMENT = 'sandbox'
    monkeypatch.setattr('apps.travelperk.connector.settings', DummySettings())


def test_connector_init_sets_refresh_token(monkeypatch):
    """
    Test TravelperkConnector __init__ sets refresh_token
    """
    cred = MagicMock()
    cred.refresh_token = 'old_token'
    mock_travelperk = MagicMock()
    mock_travelperk.refresh_token = 'new_token'
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr('apps.travelperk.connector.Travelperk', lambda *a, **kw: mock_travelperk)
    from apps.travelperk import connector
    conn = connector.TravelperkConnector(cred, 1)
    assert cred.refresh_token == 'new_token'
    monkeypatch.undo()


def test_create_webhook_success(monkeypatch):
    """
    Test create_webhook returns response and updates TravelPerk
    """
    cred = MagicMock()
    cred.refresh_token = 'token'
    mock_travelperk = MagicMock()
    mock_travelperk.refresh_token = 'token'
    monkeypatch.setattr('apps.travelperk.connector.Travelperk', lambda *a, **kw: mock_travelperk)
    from apps.travelperk import connector
    conn = connector.TravelperkConnector(cred, 1)
    conn.connection.webhooks.create.return_value = {'id': 'webhook1', 'enabled': True}
    monkeypatch.setattr('apps.travelperk.connector.TravelPerk.objects.update_or_create', MagicMock())
    resp = conn.create_webhook({'foo': 'bar'})
    assert resp['id'] == 'webhook1'


def test_create_webhook_none(monkeypatch):
    """
    Test create_webhook returns None if no response
    """
    cred = MagicMock()
    cred.refresh_token = 'token'
    mock_travelperk = MagicMock()
    mock_travelperk.refresh_token = 'token'
    monkeypatch.setattr('apps.travelperk.connector.Travelperk', lambda *a, **kw: mock_travelperk)
    from apps.travelperk import connector
    conn = connector.TravelperkConnector(cred, 1)
    conn.connection.webhooks.create.return_value = None
    resp = conn.create_webhook({'foo': 'bar'})
    assert resp is None


def test_delete_webhook_connection(monkeypatch):
    """
    Test delete_webhook_connection returns response
    """
    cred = MagicMock()
    cred.refresh_token = 'token'
    mock_travelperk = MagicMock()
    mock_travelperk.refresh_token = 'token'
    monkeypatch.setattr('apps.travelperk.connector.Travelperk', lambda *a, **kw: mock_travelperk)
    from apps.travelperk import connector
    conn = connector.TravelperkConnector(cred, 1)
    conn.connection.webhooks.delete.return_value = {'deleted': True}
    resp = conn.delete_webhook_connection('webhook1')
    assert resp['deleted'] is True


def test_sync_invoice_profile(monkeypatch):
    """
    Test sync_invoice_profile updates mappings and returns profiles
    """
    cred = MagicMock()
    cred.refresh_token = 'token'
    mock_travelperk = MagicMock()
    mock_travelperk.refresh_token = 'token'
    monkeypatch.setattr('apps.travelperk.connector.Travelperk', lambda *a, **kw: mock_travelperk)
    from apps.travelperk import connector
    conn = connector.TravelperkConnector(cred, 1)
    profile = {'billing_information': {'country_name': 'IN'}, 'currency': 'INR', 'name': 'foo', 'id': 'bar'}
    conn.connection.invoice_profiles.get_all_generator.return_value = [profile]
    monkeypatch.setattr('apps.travelperk.connector.TravelperkProfileMapping.objects.update_or_create', MagicMock())
    profiles = conn.sync_invoice_profile()
    assert profiles[0]['name'] == 'foo' 
