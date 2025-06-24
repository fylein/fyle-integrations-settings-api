import pytest
from apps.bamboohr.email import send_failure_notification_email
from tests.test_bamboohr.mock_setup import mock_sendgrid_email_shared_mock


def test_send_failure_notification_email_sends_email(mocker):
    """
    Test send_failure_notification_email sends email using SendGrid
    """
    mock_dependencies = mock_sendgrid_email_shared_mock(mocker)
    
    employees = [{'name': 'John Doe', 'id': '123'}]
    admin_email = ['admin@example.com']
    
    send_failure_notification_email(employees, 1, admin_email)
    
    mock_dependencies['mock_sendgrid'].assert_called_once()
    assert mock_dependencies['mock_sg_instance'].send.called
