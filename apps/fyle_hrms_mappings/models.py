from django.db import models
from apps.orgs.models import Org
from django.db.models import JSONField

# Create your models here.

class DestinationAttribute(models.Model):
    """
    Destination Expense Attributes
    """
    id = models.AutoField(primary_key=True)
    attribute_type = models.CharField(max_length=255, help_text='Type of expense attribute')
    org = models.ForeignKey(Org, on_delete=models.PROTECT, help_text='Reference to Org model')
    active = models.BooleanField(null=True, help_text='Indicates whether the fields is active or not')
    detail = JSONField(help_text='Detailed destination attributes payload', null=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at datetime')
    destination_id = models.CharField(max_length=255, help_text='Destination ID')
    auto_created = models.BooleanField(default=False,
                                        help_text='Indicates whether the field is auto created by the integration')


class ExpenseAttribute(models.Model):
    """
    Fyle Expense Attributes
    """
    id = models.AutoField(primary_key=True)
    org = models.ForeignKey(Org, on_delete=models.PROTECT, help_text='Reference to Org model')
    attribute_type = models.CharField(max_length=255, help_text='Type of expense attribute')
    active = models.BooleanField(null=True, help_text='Indicates whether the fields is active or not')
    detail = JSONField(help_text='Detailed expense attributes payload', null=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at datetime')
    source_id = models.CharField(max_length=255, help_text='Fyle ID')
    auto_created = models.BooleanField(default=False,
                                    help_text='Indicates whether the field is auto created by the integration')
