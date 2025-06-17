import pytest
from apps.orgs.exceptions import handle_fyle_exceptions
from fyle.platform.exceptions import InvalidTokenError

def test_handle_fyle_exceptions_decorator_logs_error(mocker):
    logger = mocker.patch('apps.orgs.exceptions.logger')

    @handle_fyle_exceptions('test_task')
    def func(org_id):
        raise InvalidTokenError()

    result = func(1)
    assert result is None
    assert logger.info.called or logger.error.called
