import pytest
from bamboosdk.exceptions import (
    BambooHrSDKError,
    NoPrivilegeError,
    NotFoundItemError,
    InvalidTokenError,
    InternalServerError
)
from .fixtures import (
    error_401_message,
    error_403_message,
    error_404_message,
    error_500_message
)


def test_bamboo_hr_sdk_error_creation():
    """
    Test BambooHrSDKError creation
    """
    error_message = "Test error message"
    error = BambooHrSDKError(error_message)
    
    assert error.message == error_message
    assert error.response is None
    assert str(error) == repr(error_message)


def test_bamboo_hr_sdk_error_with_response():
    """
    Test BambooHrSDKError creation with response
    """
    error_message = "Test error message"
    response_data = {'error': 'Test response'}
    error = BambooHrSDKError(error_message, response_data)
    
    assert error.message == error_message
    assert error.response == response_data
    assert str(error) == repr(error_message)


def test_no_privilege_error_creation():
    """
    Test NoPrivilegeError creation
    """
    error = NoPrivilegeError(error_403_message)
    
    assert error.message == error_403_message
    assert error.response is None
    assert str(error) == repr(error_403_message)
    assert isinstance(error, BambooHrSDKError)


def test_no_privilege_error_with_response():
    """
    Test NoPrivilegeError creation with response
    """
    response_data = {'error': 'Forbidden'}
    error = NoPrivilegeError(error_403_message, response_data)
    
    assert error.message == error_403_message
    assert error.response == response_data
    assert str(error) == repr(error_403_message)


def test_not_found_item_error_creation():
    """
    Test NotFoundItemError creation
    """
    error = NotFoundItemError(error_404_message)
    
    assert error.message == error_404_message
    assert error.response is None
    assert str(error) == repr(error_404_message)
    assert isinstance(error, BambooHrSDKError)


def test_not_found_item_error_with_response():
    """
    Test NotFoundItemError creation with response
    """
    response_data = {'error': 'Not Found'}
    error = NotFoundItemError(error_404_message, response_data)
    
    assert error.message == error_404_message
    assert error.response == response_data
    assert str(error) == repr(error_404_message)


def test_invalid_token_error_creation():
    """
    Test InvalidTokenError creation
    """
    error = InvalidTokenError(error_401_message)
    
    assert error.message == error_401_message
    assert error.response is None
    assert str(error) == repr(error_401_message)
    assert isinstance(error, BambooHrSDKError)


def test_invalid_token_error_with_response():
    """
    Test InvalidTokenError creation with response
    """
    response_data = {'error': 'Unauthorized'}
    error = InvalidTokenError(error_401_message, response_data)
    
    assert error.message == error_401_message
    assert error.response == response_data
    assert str(error) == repr(error_401_message)


def test_internal_server_error_creation():
    """
    Test InternalServerError creation
    """
    error = InternalServerError(error_500_message)
    
    assert error.message == error_500_message
    assert error.response is None
    assert str(error) == repr(error_500_message)
    assert isinstance(error, BambooHrSDKError)


def test_internal_server_error_with_response():
    """
    Test InternalServerError creation with response
    """
    response_data = {'error': 'Internal Server Error'}
    error = InternalServerError(error_500_message, response_data)
    
    assert error.message == error_500_message
    assert error.response == response_data
    assert str(error) == repr(error_500_message)


def test_exception_inheritance():
    """
    Test exception inheritance hierarchy
    """
    error = BambooHrSDKError("Test message")
    assert isinstance(error, Exception)
    
    no_privilege_error = NoPrivilegeError("Test message")
    assert isinstance(no_privilege_error, BambooHrSDKError)
    assert isinstance(no_privilege_error, Exception)
    
    not_found_error = NotFoundItemError("Test message")
    assert isinstance(not_found_error, BambooHrSDKError)
    assert isinstance(not_found_error, Exception)
    
    invalid_token_error = InvalidTokenError("Test message")
    assert isinstance(invalid_token_error, BambooHrSDKError)
    assert isinstance(invalid_token_error, Exception)
    
    internal_server_error = InternalServerError("Test message")
    assert isinstance(internal_server_error, BambooHrSDKError)
    assert isinstance(internal_server_error, Exception)


def test_exception_raising():
    """
    Test exception raising and catching
    """
    with pytest.raises(BambooHrSDKError) as excinfo:
        raise BambooHrSDKError("Test error")
    assert excinfo.value.message == "Test error"
    
    with pytest.raises(NoPrivilegeError) as excinfo:
        raise NoPrivilegeError("Forbidden")
    assert excinfo.value.message == "Forbidden"
    
    with pytest.raises(NotFoundItemError) as excinfo:
        raise NotFoundItemError("Not found")
    assert excinfo.value.message == "Not found"
    
    with pytest.raises(InvalidTokenError) as excinfo:
        raise InvalidTokenError("Invalid token")
    assert excinfo.value.message == "Invalid token"
    
    with pytest.raises(InternalServerError) as excinfo:
        raise InternalServerError("Server error")
    assert excinfo.value.message == "Server error"


def test_exception_catching_base_class():
    """
    Test catching specific exceptions using base class
    """
    with pytest.raises(BambooHrSDKError):
        raise NoPrivilegeError("Forbidden")
    
    with pytest.raises(BambooHrSDKError):
        raise NotFoundItemError("Not found")
    
    with pytest.raises(BambooHrSDKError):
        raise InvalidTokenError("Invalid token")
    
    with pytest.raises(BambooHrSDKError):
        raise InternalServerError("Server error") 
