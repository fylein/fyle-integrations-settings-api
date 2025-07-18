from unittest.mock import patch
from fyle.platform.exceptions import InvalidTokenError, WrongParamsError, InternalServerError

from apps.orgs.exceptions import handle_fyle_exceptions


def test_handle_fyle_exceptions_success():
    """
    Test handle_fyle_exceptions decorator with successful function execution
    """
    @handle_fyle_exceptions('test_task')
    def test_function(org_id, arg1, arg2):
        return f"success_{org_id}_{arg1}_{arg2}"
    
    result = test_function(123, 'arg1', 'arg2')
    assert result == "success_123_arg1_arg2"


def test_handle_fyle_exceptions_invalid_token_error():
    """
    Test handle_fyle_exceptions decorator with InvalidTokenError
    """
    @handle_fyle_exceptions('test_task')
    def test_function(org_id, arg1):
        raise InvalidTokenError('Invalid token')
    
    result = test_function(123, 'arg1')
    assert result is None


def test_handle_fyle_exceptions_wrong_params_error():
    """
    Test handle_fyle_exceptions decorator with WrongParamsError
    """
    @handle_fyle_exceptions('test_task')
    def test_function(org_id, arg1):
        error = WrongParamsError('Wrong parameters')
        error.message = 'Invalid parameters provided'
        error.response = {'error': 'bad_request'}
        raise error
    
    result = test_function(123, 'arg1')
    assert result is None


def test_handle_fyle_exceptions_internal_server_error():
    """
    Test handle_fyle_exceptions decorator with InternalServerError
    """
    @handle_fyle_exceptions('test_task')
    def test_function(org_id, arg1):
        error = InternalServerError('Internal server error')
        error.__dict__ = {'status_code': 500, 'message': 'Server error'}
        raise error
    
    result = test_function(123, 'arg1')
    assert result is None


def test_handle_fyle_exceptions_generic_exception():
    """
    Test handle_fyle_exceptions decorator with generic Exception
    """
    @handle_fyle_exceptions('test_task')
    def test_function(org_id, arg1):
        raise ValueError('Some unexpected error')
    
    result = test_function(123, 'arg1')
    assert result is None


def test_handle_fyle_exceptions_with_logging():
    """
    Test handle_fyle_exceptions decorator with logging verification
    """
    with patch('apps.orgs.exceptions.logger') as mock_logger:
        @handle_fyle_exceptions('test_task')
        def test_function(org_id, arg1):
            raise InvalidTokenError('Invalid token')
        
        test_function(123, 'arg1')
        
        # Verify logger.info was called with the error details
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert call_args['task'] == 'test_task'
        assert call_args['org_id'] == 123
        assert call_args['message'] == 'Invalid Fyle refresh token'
        assert call_args['alert'] is False


def test_handle_fyle_exceptions_with_alert_logging():
    """
    Test handle_fyle_exceptions decorator with alert logging for WrongParamsError
    """
    with patch('apps.orgs.exceptions.logger') as mock_logger:
        @handle_fyle_exceptions('test_task')
        def test_function(org_id, arg1):
            error = WrongParamsError('Wrong parameters')
            error.message = 'Invalid parameters provided'
            error.response = {'error': 'bad_request'}
            raise error
        
        test_function(123, 'arg1')
        
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert call_args['task'] == 'test_task'
        assert call_args['org_id'] == 123
        assert call_args['message'] == 'Invalid parameters provided'
        assert call_args['response'] == {'error': 'bad_request'}
        assert call_args['alert'] is True


def test_handle_fyle_exceptions_with_generic_exception_logging():
    """
    Test handle_fyle_exceptions decorator with generic exception logging
    """
    with patch('apps.orgs.exceptions.logger') as mock_logger:
        @handle_fyle_exceptions('test_task')
        def test_function(org_id, arg1):
            raise ValueError('Some unexpected error')
        
        test_function(123, 'arg1')
        
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert call_args['task'] == 'test_task'
        assert call_args['org_id'] == 123
        assert call_args['message'] == 'Something went wrong'
        assert 'Traceback' in call_args['response']
        assert call_args['alert'] is True


def test_handle_fyle_exceptions_decorator_returns_function():
    """
    Test that handle_fyle_exceptions decorator returns a callable function
    """
    @handle_fyle_exceptions('test_task')
    def test_function(org_id, arg1):
        return f"success_{org_id}_{arg1}"
    
    assert callable(test_function)
    
    result = test_function(123, 'test_arg')
    assert result == "success_123_test_arg"
