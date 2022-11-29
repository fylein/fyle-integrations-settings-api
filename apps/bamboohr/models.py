from django.db import models

from apps.orgs.models import Org


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

    class Meta:
        db_table = 'bamboohr'
