import pytest
from apps.orgs.exceptions import handle_fyle_exceptions
from fyle.platform.exceptions import InvalidTokenError
from .mock_setup import mock_logger_shared_mock


def test_handle_fyle_exceptions_decorator_logs_error(mocker):
    """
    Test handle_fyle_exceptions decorator logs error correctly
    """
    # Use centralized mock setup
    mock_dependencies = mock_logger_shared_mock(mocker)

    @handle_fyle_exceptions('test_task')
    def func(org_id):
        raise InvalidTokenError()

    result = func(1)
    assert result is None
    assert mock_dependencies['mock_logger'].info.called or mock_dependencies['mock_logger'].error.called
