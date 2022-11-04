from django.db import models
from apps.orgs.models import Org

# Create your models here.
class BambooHr(models.Model):
    """
    Bamboo HR Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Org')
    org = models.ManyToManyField(Org, help_text='Reference to Org table')
    api_token = models.CharField(max_length=255, help_text='Bamboo HR API Token')
    sub_domain = models.CharField(max_length=255, help_text='Bamboo HR Sub Domain')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at =  models.DateTimeField(auto_now=True, help_text='Updated at datetime')

    class Meta:
        db_table = 'orgs'


