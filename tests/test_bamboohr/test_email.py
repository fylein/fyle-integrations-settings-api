import pytest
from unittest.mock import mock_open
import sendgrid
from sendgrid.helpers.mail import Mail

from apps.bamboohr.email import send_failure_notification_email
from .fixtures import (
    failed_employees_data,
    admin_email_list,
    number_of_employees,
    email_template_content
)


def test_send_failure_notification_email(mock_dependencies):
    """
    Test send_failure_notification_email
    """
    mock_open_file = mock_open(read_data=email_template_content)
    mock_dependencies.open.return_value.__enter__.return_value = mock_open_file.return_value
    
    send_failure_notification_email(
        failed_employees_data, 
        number_of_employees, 
        admin_email_list
    )
    
    mock_dependencies.open.assert_called_once_with('apps/bamboohr/templates/mail_template.html', 'r')
    mock_dependencies.sendgrid_client.send.assert_called_once()
    
    call_args = mock_dependencies.sendgrid_client.send.call_args[0][0]
    assert isinstance(call_args, Mail)
    assert call_args.subject.subject == 'Error Importing Employees from Bamboo HR to Fyle'
    
    mock_dependencies.open.assert_called_once_with('apps/bamboohr/templates/mail_template.html', 'r')
    mock_dependencies.sendgrid_api.assert_called_once() 
