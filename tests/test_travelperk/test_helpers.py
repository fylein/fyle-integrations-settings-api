import pytest
from apps.travelperk import helpers
from unittest.mock import MagicMock
from .fixtures import fixture


def test_get_refresh_token_using_auth_code_success(mocker, mock_settings, db):
    """
    Test get_refresh_token_using_auth_code
    Case: returns refresh token on 200 response
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"refresh_token": "abc123"}'
    mock_post = mocker.patch('apps.travelperk.helpers.requests.post', return_value=mock_response)
    mock_org = mocker.patch('apps.travelperk.helpers.Org.objects.get')
    mock_update = mocker.patch('apps.travelperk.helpers.TravelperkCredential.objects.update_or_create', return_value=(MagicMock(), True))
    result = helpers.get_refresh_token_using_auth_code('code', 1)
    assert result == 'abc123'
    mock_post.assert_called_once()
    mock_org.assert_called_once()
    mock_update.assert_called_once()


def test_get_refresh_token_using_auth_code_error(mocker, mock_settings):
    """
    Test get_refresh_token_using_auth_code
    Case: raises Exception on non-200 response
    """
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = '{"error": "bad_request"}'
    mocker.patch('apps.travelperk.helpers.requests.post', return_value=mock_response)
    with pytest.raises(Exception) as exc:
        helpers.get_refresh_token_using_auth_code('code', 1)
    assert 'bad_request' in str(exc.value)


def test_download_file_success(mocker):
    """
    Test download_file
    Case: successful download returns BytesIO object
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'file content'
    mocker.patch('apps.travelperk.helpers.requests.get', return_value=mock_response)
    result = helpers.download_file('http://example.com/file.pdf')
    assert result.read() == b'file content'


def test_download_file_failure(mocker):
    """
    Test download_file
    Case: failed download returns None
    """
    mock_response = MagicMock()
    mock_response.status_code = 404
    mocker.patch('apps.travelperk.helpers.requests.get', return_value=mock_response)
    result = helpers.download_file('http://example.com/file.pdf')
    assert result is None


def test_upload_to_s3_presigned_url_success(mocker):
    """
    Test upload_to_s3_presigned_url
    Case: successful upload logs success
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mocker.patch('apps.travelperk.helpers.requests.put', return_value=mock_response)
    helpers.upload_to_s3_presigned_url(b'content', 'http://s3-url.com')


def test_upload_to_s3_presigned_url_failure(mocker):
    """
    Test upload_to_s3_presigned_url
    Case: failed upload logs error
    """
    mock_response = MagicMock()
    mock_response.status_code = 500
    mocker.patch('apps.travelperk.helpers.requests.put', return_value=mock_response)
    helpers.upload_to_s3_presigned_url(b'content', 'http://s3-url.com')


def test_get_employee_email_found(mock_conn):
    """
    Test get_employee_email
    Case: employee found
    """
    mock_conn.v1.admin.employees.list.return_value = {'data': [{'user': {'email': 'foo@bar.com'}}]}
    result = helpers.get_employee_email(mock_conn, 'foo@bar.com')
    assert result == 'foo@bar.com'


def test_get_employee_email_not_found(mock_conn):
    """
    Test get_employee_email
    Case: employee not found
    """
    mock_conn.v1.admin.employees.list.return_value = {'data': []}
    result = helpers.get_employee_email(mock_conn, 'foo@bar.com')
    assert result is None


def test_check_for_transaction_in_fyle(mock_conn, mock_expense):
    """
    Test check_for_transaction_in_fyle
    Case: returns expense details
    """
    mock_conn.v1.admin.corporate_card_transactions.list.return_value = {'data': [{'id': 'tx1'}]}
    result = helpers.check_for_transaction_in_fyle(mock_conn, mock_expense, 'card1', 100)
    assert result == [{'id': 'tx1'}]


def test_check_for_transaction_in_fyle_empty(mock_conn, mock_expense):
    """
    Test check_for_transaction_in_fyle
    Case: returns empty list if no transactions
    """
    mock_conn.v1.admin.corporate_card_transactions.list.return_value = {'data': []}
    result = helpers.check_for_transaction_in_fyle(mock_conn, mock_expense, 'card1', 100)
    assert result == []


def test_get_email_from_credit_card_and_match_transaction_with_user_id(mock_conn, mock_expense):
    """
    Test get_email_from_credit_card_and_match_transaction
    Case: user_id found, no matched transaction
    """
    mock_conn.v1.admin.corporate_cards.list.return_value = {'data': [{'user_id': 'user1', 'id': 'card1'}]}
    mock_conn.v1.admin.corporate_card_transactions.list.return_value = {'data': []}
    mock_conn.v1.admin.employees.list.return_value = {'data': [{'user': {'email': 'user@example.com'}}]}
    email, matched = helpers.get_email_from_credit_card_and_match_transaction(mock_conn, mock_expense, 100)
    assert email == 'user@example.com'
    assert matched == []


def test_get_email_from_credit_card_and_match_transaction_no_user_id(mock_conn, mock_expense):
    """
    Test get_email_from_credit_card_and_match_transaction
    Case: no user_id found
    """
    mock_conn.v1.admin.corporate_cards.list.return_value = {'data': []}
    mock_conn.v1.admin.corporate_card_transactions.list.return_value = {'data': []}
    email, matched = helpers.get_email_from_credit_card_and_match_transaction(mock_conn, mock_expense, 100)
    assert email is None
    assert matched == []


def test_get_email_from_credit_card_and_match_transaction_with_matched_transaction(mock_conn, mock_expense):
    """
    Test get_email_from_credit_card_and_match_transaction
    Case: matched transaction found
    """
    mock_conn.v1.admin.corporate_cards.list.return_value = {'data': [{'user_id': 'user1', 'id': 'card1'}]}
    mock_conn.v1.admin.corporate_card_transactions.list.return_value = {'data': [{'id': 'tx1'}]}
    email, matched = helpers.get_email_from_credit_card_and_match_transaction(mock_conn, mock_expense, 100)
    assert email is None
    assert matched == [{'id': 'tx1'}]


def test_construct_file_ids(mocker):
    """
    Test construct_file_ids
    Case: returns file id list
    """
    mock_platform = MagicMock()
    mock_platform.v1.spender.files.create_file.return_value = {'data': {'id': 'file123'}}
    mock_platform.v1.spender.files.generate_file_urls.return_value = {'data': {'upload_url': 'http://upload'}}
    mocker.patch('apps.travelperk.helpers.download_file', return_value=b'data')
    mocker.patch('apps.travelperk.helpers.upload_to_s3_presigned_url')
    result = helpers.construct_file_ids(mock_platform, 'http://test.pdf')
    assert result == ['file123'] 
 