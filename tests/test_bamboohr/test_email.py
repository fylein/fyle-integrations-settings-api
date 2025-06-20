import pytest
from unittest.mock import patch, MagicMock, mock_open
import base64
import csv
from io import StringIO

from apps.bamboohr.email import send_failure_notification_email


@pytest.mark.django_db
class TestBambooHrEmail:
    def test_send_failure_notification_email(self, mocker):
        """Test send_failure_notification_email function"""
        # Mock the template file read
        mock_template = """
        <html>
            <body>
                <p>Failed to import {number_of_employees} employees</p>
            </body>
        </html>
        """
        mock_file = mock_open(read_data=mock_template)
        
        # Mock sendgrid
        mock_sendgrid = mocker.patch('apps.bamboohr.email.sendgrid.SendGridAPIClient')
        mock_sg_instance = MagicMock()
        mock_sendgrid.return_value = mock_sg_instance
        
        # Mock settings
        mock_settings = mocker.patch('apps.bamboohr.email.settings')
        mock_settings.SENDGRID_EMAIL = 'test@example.com'
        mock_settings.SENDGRID_API_KEY = 'test_api_key'
        
        # Test data
        employees = [
            {'id': 1, 'name': 'John Doe'},
            {'id': 2, 'name': 'Jane Smith'}
        ]
        number_of_employees = 2
        admin_email = ['admin@example.com']
        
        with patch('builtins.open', mock_file):
            send_failure_notification_email(employees, number_of_employees, admin_email)
        
        # Verify file was opened correctly
        mock_file.assert_called_once_with('apps/bamboohr/templates/mail_template.html', 'r')
        
        # Verify sendgrid was called
        mock_sendgrid.assert_called_once_with(api_key='test_api_key')
        
        # Verify send was called
        mock_sg_instance.send.assert_called_once()

    def test_send_failure_notification_email_empty_employees(self, mocker):
        """Test send_failure_notification_email with empty employees list"""
        # Mock the template file read
        mock_template = """
        <html>
            <body>
                <p>Failed to import {number_of_employees} employees</p>
            </body>
        </html>
        """
        mock_file = mock_open(read_data=mock_template)
        
        # Mock sendgrid
        mock_sendgrid = mocker.patch('apps.bamboohr.email.sendgrid.SendGridAPIClient')
        mock_sg_instance = MagicMock()
        mock_sendgrid.return_value = mock_sg_instance
        
        # Mock settings
        mock_settings = mocker.patch('apps.bamboohr.email.settings')
        mock_settings.SENDGRID_EMAIL = 'test@example.com'
        mock_settings.SENDGRID_API_KEY = 'test_api_key'
        
        # Test data
        employees = []
        number_of_employees = 0
        admin_email = ['admin@example.com']
        
        with patch('builtins.open', mock_file):
            send_failure_notification_email(employees, number_of_employees, admin_email)
        
        # Verify send was called
        mock_sg_instance.send.assert_called_once()

    def test_send_failure_notification_email_multiple_admin_emails(self, mocker):
        """Test send_failure_notification_email with multiple admin emails"""
        # Mock the template file read
        mock_template = """
        <html>
            <body>
                <p>Failed to import {number_of_employees} employees</p>
            </body>
        </html>
        """
        mock_file = mock_open(read_data=mock_template)
        
        # Mock sendgrid
        mock_sendgrid = mocker.patch('apps.bamboohr.email.sendgrid.SendGridAPIClient')
        mock_sg_instance = MagicMock()
        mock_sendgrid.return_value = mock_sg_instance
        
        # Mock settings
        mock_settings = mocker.patch('apps.bamboohr.email.settings')
        mock_settings.SENDGRID_EMAIL = 'test@example.com'
        mock_settings.SENDGRID_API_KEY = 'test_api_key'
        
        # Test data
        employees = [{'id': 1, 'name': 'John Doe'}]
        number_of_employees = 1
        admin_email = ['admin1@example.com', 'admin2@example.com']
        
        with patch('builtins.open', mock_file):
            send_failure_notification_email(employees, number_of_employees, admin_email)
        
        # Verify send was called
        mock_sg_instance.send.assert_called_once()
        # The function should not raise any exceptions
