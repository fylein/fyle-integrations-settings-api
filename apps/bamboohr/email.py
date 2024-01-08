import csv
from io import StringIO
from typing import List

import sendgrid
from sendgrid.helpers.mail import Mail, Attachment
from python_http_client.exceptions import HTTPError
import base64

from admin_settings import settings

def send_failure_notification_email(employees: List[dict], number_of_employees: int ,admin_email: str):

    with open('apps/bamboohr/templates/mail_template.html', 'r') as file:
        email_template = file.read()
    
    email_content_html = email_template.format_map({'number_of_employees':number_of_employees})

    csv_file = StringIO()
    csv_writer = csv.DictWriter(csv_file, fieldnames=['id', 'name'])
    csv_writer.writeheader()
    csv_writer.writerows(employees)

    csv_content_base64 = base64.b64encode(csv_file.getvalue().encode()).decode()

    message = Mail(
        from_email=settings.SENDGRID_EMAIL,  
        to_emails=admin_email,
        subject='Error Importing Employees from Bamboo HR to Fyle',
        html_content=email_content_html
    )

    attachment = Attachment()
    attachment.file_content = csv_content_base64
    attachment.file_name = 'employee_data.csv'
    attachment.file_type = 'text/csv'
    attachment.disposition = 'attachment'
    message.attachment = attachment

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    sg.send(message)

