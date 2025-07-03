import pytest
from io import BytesIO

from apps.travelperk.helpers import (
    get_refresh_token_using_auth_code,
    download_file,
    upload_to_s3_presigned_url,
    get_employee_email,
    check_for_transaction_in_fyle,
    get_email_from_credit_card_and_match_transaction,
    construct_file_ids
)
from .mock_setup import (
    mock_test_get_refresh_token_case_1,
    mock_test_get_refresh_token_case_2,
    mock_test_download_file_case_1,
    mock_test_download_file_case_2,
    mock_test_upload_to_s3_case_1,
    mock_test_get_employee_email_case_1,
    mock_test_get_employee_email_case_2,
    mock_test_check_transaction_case_1,
    mock_test_get_email_from_card_case_1,
    mock_test_get_email_from_card_case_2,
    mock_test_construct_file_ids_case_1
)
from .fixtures import (
    test_refresh_token,
    test_code,
    invalid_code,
    test_employee_email,
    nonexistent_employee_email,
    test_amount,
    test_card_id,
    test_url,
    test_presigned_url,
    test_file_content
)


@pytest.mark.shared_mocks(lambda mocker: mock_test_get_refresh_token_case_1(mocker))
def test_get_refresh_token_case_1(mock_dependencies, create_org):
    """
    Test get_refresh_token_using_auth_code
    Case: Successful token exchange
    """
    result = get_refresh_token_using_auth_code(test_code, create_org.id)
    
    assert result == test_refresh_token
    mock_dependencies.requests_post.assert_called_once()
    mock_dependencies.update_or_create.assert_called_once()


@pytest.mark.shared_mocks(lambda mocker: mock_test_get_refresh_token_case_2(mocker))
def test_get_refresh_token_case_2(mock_dependencies, create_org):
    """
    Test get_refresh_token_using_auth_code
    Case: API returns error status
    """
    with pytest.raises(Exception):
        get_refresh_token_using_auth_code(invalid_code, create_org.id)


@pytest.mark.shared_mocks(lambda mocker: mock_test_download_file_case_1(mocker))
def test_download_file_case_1(mock_dependencies):
    """
    Test download_file function
    Case: Successful file download
    """
    result = download_file(test_url)
    
    assert isinstance(result, BytesIO)
    mock_dependencies.requests_get.assert_called_once_with(test_url, stream=True)


@pytest.mark.shared_mocks(lambda mocker: mock_test_download_file_case_2(mocker))
def test_download_file_case_2(mock_dependencies):
    """
    Test download_file function
    Case: Failed file download
    """
    result = download_file('https://example.com/nonexistent.pdf')
    
    assert result is None
    mock_dependencies.requests_get.assert_called_once()


@pytest.mark.shared_mocks(lambda mocker: mock_test_upload_to_s3_case_1(mocker))
def test_upload_to_s3_case_1(mock_dependencies):
    """
    Test upload_to_s3_presigned_url function
    Case: Successful upload
    """
    upload_to_s3_presigned_url(test_file_content, test_presigned_url)
    
    mock_dependencies.requests_put.assert_called_once()


@pytest.mark.shared_mocks(lambda mocker: mock_test_get_employee_email_case_1(mocker))
def test_get_employee_email_case_1(mock_dependencies):
    """
    Test get_employee_email function
    Case: Employee found
    """
    result = get_employee_email(mock_dependencies.platform_connection, test_employee_email)
    
    assert result == test_employee_email
    mock_dependencies.platform_connection.v1.admin.employees.list.assert_called_once()


@pytest.mark.shared_mocks(lambda mocker: mock_test_get_employee_email_case_2(mocker))
def test_get_employee_email_case_2(mock_dependencies):
    """
    Test get_employee_email function
    Case: Employee not found
    """
    result = get_employee_email(mock_dependencies.platform_connection, nonexistent_employee_email)
    
    assert result is None


@pytest.mark.shared_mocks(lambda mocker: mock_test_check_transaction_case_1(mocker))
def test_check_transaction_case_1(mock_dependencies):
    """
    Test check_for_transaction_in_fyle function
    Case: Transaction found
    """
    expense = mock_dependencies.expense
    result = check_for_transaction_in_fyle(mock_dependencies.platform_connection, expense, test_card_id, test_amount)
    
    assert len(result) == 1
    mock_dependencies.platform_connection.v1.admin.corporate_card_transactions.list.assert_called_once()


@pytest.mark.shared_mocks(lambda mocker: mock_test_get_email_from_card_case_1(mocker))
def test_get_email_from_card_case_1(mock_dependencies):
    """
    Test get_email_from_credit_card_and_match_transaction function
    Case: Card found, no matched transaction
    """
    expense = mock_dependencies.expense
    email, matched_transaction = get_email_from_credit_card_and_match_transaction(
        mock_dependencies.platform_connection, expense, test_amount
    )
    
    assert email == test_employee_email
    assert matched_transaction == []


@pytest.mark.shared_mocks(lambda mocker: mock_test_get_email_from_card_case_2(mocker))
def test_get_email_from_card_case_2(mock_dependencies):
    """
    Test get_email_from_credit_card_and_match_transaction function
    Case: Card not found
    """
    expense = mock_dependencies.expense
    email, matched_transaction = get_email_from_credit_card_and_match_transaction(
        mock_dependencies.platform_connection, expense, test_amount
    )
    
    assert email is None
    assert matched_transaction == []


@pytest.mark.shared_mocks(lambda mocker: mock_test_construct_file_ids_case_1(mocker))
def test_construct_file_ids_case_1(mock_dependencies):
    """
    Test construct_file_ids function
    Case: Successfully creates file and uploads
    """
    result = construct_file_ids(mock_dependencies.platform_connection, test_url)
    
    assert result == ['file_123']
    mock_dependencies.platform_connection.v1.spender.files.create_file.assert_called_once()
    mock_dependencies.platform_connection.v1.spender.files.generate_file_urls.assert_called_once() 
