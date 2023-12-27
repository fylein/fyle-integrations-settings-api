from django.db import models

from apps.orgs.models import Org
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField

class BambooHr(models.Model):
    """
    Bamboo HR Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Org')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org table')
    folder_id = models.CharField(max_length=255, null=True, help_text='Bamboo HR Folder ID')
    package_id = models.CharField(max_length=255, null=True, help_text="Bamboo HR Package ID")
    api_token = models.CharField(max_length=255, null=True, help_text='Bamboo HR API Token')
    sub_domain = models.CharField(max_length=255, null=True, help_text='Bamboo HR Sub Domain')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at =  models.DateTimeField(auto_now=True, help_text='Updated at datetime')
    employee_exported_at = models.DateTimeField(auto_now_add=True, help_text='Employee exported to Fyle at datetime')

    class Meta:
        db_table = 'bamboohr'


class BambooHrConfiguration(models.Model):
    """
    BambooHr Configuration Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Configuration')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org Table')
    recipe_id = models.CharField(max_length=255, help_text='Recipe Id', null=True)
    recipe_data = models.TextField(help_text='Code For Recipe', null=True)
    recipe_status = models.BooleanField(help_text='recipe status', null=True)
    additional_email_options = JSONField(default=list, help_text='Email and Name of person to send email', null=True)
    emails_selected = JSONField(default=list, help_text='Emails Selected For Email Notification',  null=True)

    class Meta:
        db_table = 'bamboohr_configurations'
