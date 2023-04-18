from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Org(models.Model):
    """
    Org Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Org')
    name = models.CharField(max_length=255, help_text='Name of the org')
    user = models.ManyToManyField(User, help_text='Reference to users table')
    fyle_org_id = models.CharField(max_length=255, help_text='org id', unique=True)
    managed_user_id = models.CharField(max_length=255, null=True, help_text='Managed User Id')
    cluster_domain = models.CharField(max_length=255, help_text='Fyle cluster domain')
    is_fyle_connected = models.BooleanField(null=True, help_text='Is Fyle API Connected')
    is_sendgrid_connected = models.BooleanField(null=True, help_text='Is Sendgrid Connected')
    allow_travelperk = models.BooleanField(default=False, help_text='Allow Travelperk')
    allow_gusto = models.BooleanField(default=False, help_text='Allow Gusto')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at =  models.DateTimeField(auto_now=True, help_text='Updated at datetime')

    class Meta:
        db_table = 'orgs'


class FyleCredential(models.Model):
    """
    Table to store Fyle credentials
    """
    id = models.AutoField(primary_key=True)
    refresh_token = models.TextField(help_text='Stores Fyle refresh token')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org model')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at datetime')

    class Meta:
        db_table = 'fyle_credentials'

