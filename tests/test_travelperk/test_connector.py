import pytest

from apps.travelperk.connector import TravelperkConnector
from apps.travelperk.models import TravelPerk, TravelperkProfileMapping
from .fixtures import (
    webhook_create_data,
    webhook_response_data,
    webhook_delete_response,
    test_webhook_subscription_id,
    test_profile_id_1,
    test_profile_id_2,
    test_profile_name_1,
    test_profile_name_2,
    test_currency_usd,
    test_currency_eur,
    test_country_us,
    test_country_germany,
    test_refresh_token_updated
)
from .mock_setup import (
    mock_test_travelperk_connector_init_case_1,
    mock_test_connector_create_webhook_case_1,
    mock_test_connector_create_webhook_case_2,
    mock_test_connector_delete_webhook_case_1,
    mock_test_connector_sync_invoice_profile_case_1,
    mock_test_connector_sync_invoice_profile_case_2,
    mock_test_connector_sync_invoice_profile_case_3
)


@pytest.mark.shared_mocks(lambda mocker: mock_test_travelperk_connector_init_case_1(mocker))
def test_travelperk_connector_init_case_1(mock_dependencies, create_travelperk_full_setup):
    """
    Test TravelperkConnector initialization
    Case: Successfully initializes connector and updates refresh token
    """
    setup = create_travelperk_full_setup
    credential = setup['credential']
    
    connector = TravelperkConnector(credential, setup['org'].id)
    
    assert connector.org_id == setup['org'].id
    assert connector.connection is not None
    
    credential.refresh_from_db()
    assert credential.refresh_token == test_refresh_token_updated


@pytest.mark.shared_mocks(lambda mocker: mock_test_connector_create_webhook_case_1(mocker))
def test_create_webhook_case_1(mock_dependencies, create_travelperk_full_setup):
    """
    Test create_webhook method
    Case: Successfully creates webhook and updates TravelPerk model
    """
    setup = create_travelperk_full_setup
    credential = setup['credential']
    
    connector = TravelperkConnector(credential, setup['org'].id)
    result = connector.create_webhook(webhook_create_data)
    
    assert result == webhook_response_data
    assert result['id'] == test_webhook_subscription_id
    assert result['enabled'] is True
    
    # Verify TravelPerk model was updated in database
    setup['travelperk'].refresh_from_db()
    assert setup['travelperk'].webhook_subscription_id == webhook_response_data['id']
    assert setup['travelperk'].webhook_enabled == webhook_response_data['enabled']


@pytest.mark.shared_mocks(lambda mocker: mock_test_connector_create_webhook_case_2(mocker))
def test_create_webhook_case_2(mock_dependencies, create_travelperk_full_setup):
    """
    Test create_webhook method
    Case: Returns None when webhook creation fails
    """
    setup = create_travelperk_full_setup
    credential = setup['credential']
    
    connector = TravelperkConnector(credential, setup['org'].id)
    result = connector.create_webhook(webhook_create_data)
    
    assert result is None


@pytest.mark.shared_mocks(lambda mocker: mock_test_connector_delete_webhook_case_1(mocker))
def test_delete_webhook_case_1(mock_dependencies, create_travelperk_full_setup):
    """
    Test delete_webhook_connection method
    Case: Successfully deletes webhook
    """
    setup = create_travelperk_full_setup
    credential = setup['credential']
    
    connector = TravelperkConnector(credential, setup['org'].id)
    result = connector.delete_webhook_connection(test_webhook_subscription_id)
    
    assert result == webhook_delete_response
    mock_dependencies.travelperk_instance.webhooks.delete.assert_called_once_with(test_webhook_subscription_id)


@pytest.mark.shared_mocks(lambda mocker: mock_test_connector_sync_invoice_profile_case_1(mocker))
def test_sync_invoice_profile_case_1(mock_dependencies, create_travelperk_full_setup):
    """
    Test sync_invoice_profile method
    Case: Successfully syncs multiple invoice profiles with complete data
    """
    setup = create_travelperk_full_setup
    credential = setup['credential']
    
    connector = TravelperkConnector(credential, setup['org'].id)
    result = connector.sync_invoice_profile()
    
    assert len(result) == 2
    assert result[0]['id'] == test_profile_id_1
    assert result[0]['name'] == test_profile_name_1
    assert result[0]['currency'] == test_currency_usd
    assert result[0]['billing_information']['country_name'] == test_country_us
    
    assert result[1]['id'] == test_profile_id_2
    assert result[1]['name'] == test_profile_name_2
    assert result[1]['currency'] == test_currency_eur
    assert result[1]['billing_information']['country_name'] == test_country_germany
    
    # Verify TravelperkProfileMapping records were created in database
    profile_mappings = TravelperkProfileMapping.objects.filter(org=setup['org'])
    assert profile_mappings.count() >= 2  # At least 2 new mappings
    
    profile1 = TravelperkProfileMapping.objects.filter(
        org=setup['org'], 
        profile_name=test_profile_name_1,
        source_id=test_profile_id_1
    ).first()
    assert profile1 is not None
    assert profile1.country == test_country_us
    assert profile1.currency == test_currency_usd
    
    profile2 = TravelperkProfileMapping.objects.filter(
        org=setup['org'], 
        profile_name=test_profile_name_2,
        source_id=test_profile_id_2
    ).first()
    assert profile2 is not None
    assert profile2.country == test_country_germany
    assert profile2.currency == test_currency_eur


@pytest.mark.shared_mocks(lambda mocker: mock_test_connector_sync_invoice_profile_case_2(mocker))
def test_sync_invoice_profile_case_2(mock_dependencies, create_travelperk_full_setup):
    """
    Test sync_invoice_profile method
    Case: Handles profile with missing country_name field
    """
    setup = create_travelperk_full_setup
    credential = setup['credential']
    
    connector = TravelperkConnector(credential, setup['org'].id)
    result = connector.sync_invoice_profile()
    
    assert len(result) == 1
    assert result[0]['id'] == 'profile_789'
    assert result[0]['name'] == 'Test Profile No Country'
    assert result[0]['currency'] == 'GBP'
    assert 'country_name' not in result[0]['billing_information']
    
    # Verify TravelperkProfileMapping record was created in database
    profile_mapping = TravelperkProfileMapping.objects.filter(
        org=setup['org'], 
        profile_name='Test Profile No Country',
        source_id='profile_789'
    ).first()
    assert profile_mapping is not None
    assert profile_mapping.country is None
    assert profile_mapping.currency == 'GBP'


@pytest.mark.shared_mocks(lambda mocker: mock_test_connector_sync_invoice_profile_case_3(mocker))
def test_sync_invoice_profile_case_3(mock_dependencies, create_travelperk_full_setup):
    """
    Test sync_invoice_profile method
    Case: Handles profile with missing currency field
    """
    setup = create_travelperk_full_setup
    credential = setup['credential']
    
    connector = TravelperkConnector(credential, setup['org'].id)
    result = connector.sync_invoice_profile()
    
    assert len(result) == 1
    assert result[0]['id'] == 'profile_999'
    assert result[0]['name'] == 'Test Profile No Currency'
    assert 'currency' not in result[0]
    assert result[0]['billing_information']['country_name'] == 'Canada'
    
    # Verify TravelperkProfileMapping record was created in database
    profile_mapping = TravelperkProfileMapping.objects.filter(
        org=setup['org'], 
        profile_name='Test Profile No Currency',
        source_id='profile_999'
    ).first()
    assert profile_mapping is not None
    assert profile_mapping.country == 'Canada'
    assert profile_mapping.currency is None 
