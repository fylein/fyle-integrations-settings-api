from typing import Dict, List
from django.db import models
from apps.orgs.models import Org
from django.db.models import JSONField
from datetime import datetime

# Create your models here.

class DestinationAttribute(models.Model):
    """
    Destination Expense Attributes
    """
    id = models.AutoField(primary_key=True)
    attribute_type = models.CharField(max_length=255, help_text='Type of expense attribute')
    value = models.CharField(max_length=255, help_text='Value of expense attribute')
    org = models.ForeignKey(Org, on_delete=models.PROTECT, help_text='Reference to Org model')
    active = models.BooleanField(null=True, help_text='Indicates whether the fields is active or not')
    detail = JSONField(help_text='Detailed destination attributes payload', null=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at datetime')
    destination_id = models.CharField(max_length=255, help_text='Destination ID')
    auto_created = models.BooleanField(default=False,
                                        help_text='Indicates whether the field is auto created by the integration')
    is_failure_email_sent = models.BooleanField(default=False, help_text='Indicates whether the failure email is sent')

    class Meta:
        db_table = 'destination_attributes'
        unique_together = ('destination_id', 'attribute_type', 'org')

    @staticmethod
    def create_or_update_destination_attribute(attribute: Dict, org_id):
        """
        get or create destination attributes
        """
        destination_attribute, _ = DestinationAttribute.objects.update_or_create(
            attribute_type=attribute['attribute_type'],
            destination_id=attribute['destination_id'],
            org_id=org_id,
            defaults={
                'active': attribute['active'] if 'active' in attribute else None,
                'value': attribute['value'],
                'detail': attribute['detail'] if 'detail' in attribute else None
            }
        )
        return destination_attribute
    
    @staticmethod
    def bulk_create_or_update_destination_attributes(
            attributes: List[Dict], attribute_type: str, org_id: int, update: bool = False):
        """
        Create Destination Attributes in bulk
        :param update: Update Pre-existing records or not
        :param attribute_type: Attribute type
        :param attributes: attributes = [{
            'attribute_type': Type of attribute,
            'value': Value of attribute,
            'destination_id': Destination Id of the attribute,
            'detail': Extra Details of the attribute
        }]
        :param org_id: Org Id
        :return: created / updated attributes
        """
        attribute_destination_id_list = [attribute['destination_id'] for attribute in attributes]

        filters = {
            'destination_id__in': attribute_destination_id_list,
            'attribute_type': attribute_type,
            'org_id': org_id
        }

        existing_attributes = DestinationAttribute.objects.filter(**filters)\
            .values('id', 'destination_id', 'value', 'detail', 'active', 'is_failure_email_sent')

        existing_attribute_destination_ids = []

        primary_key_map = {}

        for existing_attribute in existing_attributes:
            existing_attribute_destination_ids.append(existing_attribute['destination_id'])
            primary_key_map[existing_attribute['destination_id']] = {
                'id': existing_attribute['id'],
                'value': existing_attribute['value'],
                'detail': existing_attribute['detail'],
                'active': existing_attribute['active'],
                'is_failure_email_sent': existing_attribute['is_failure_email_sent']
            }

        attributes_to_be_created = []
        attributes_to_be_updated = []

        destination_ids_appended = []
        for attribute in attributes:
            if attribute['destination_id'] not in existing_attribute_destination_ids \
                    and attribute['destination_id'] not in destination_ids_appended:
                destination_ids_appended.append(attribute['destination_id'])
                attributes_to_be_created.append(
                    DestinationAttribute(
                        attribute_type=attribute_type,
                        value=attribute['value'],
                        destination_id=attribute['destination_id'],
                        detail=attribute['detail'] if 'detail' in attribute else None,
                        org_id=org_id,
                        active=attribute['active'] if 'active' in attribute else None,
                        is_failure_email_sent=attribute['is_failure_email_sent'] if 'is_failure_email_sent' in attribute else False
                    )
                )
            else:
                if update and (
                        (attribute['value'] != primary_key_map[attribute['destination_id']]['value'])
                        or
                        ('detail' in attribute and attribute['detail'] != primary_key_map[attribute['destination_id']]['detail'])
                        or
                        ('active' in attribute and attribute['active'] != primary_key_map[attribute['destination_id']]['active'])
                        or
                        (
                            'is_failure_email_sent' in attribute and attribute['is_failure_email_sent'] != primary_key_map[attribute['destination_id']]['is_failure_email_sent']
                        )
                    ):
                        attributes_to_be_updated.append(
                            DestinationAttribute(
                                id=primary_key_map[attribute['destination_id']]['id'],
                                value=attribute['value'],
                                detail=attribute['detail'] if 'detail' in attribute else None,
                                active=attribute['active'] if 'active' in attribute else None,
                                is_failure_email_sent=attribute['is_failure_email_sent'] if 'is_failure_email_sent' in attribute else False,
                                updated_at=datetime.now(),
                            )
                        )
        if attributes_to_be_created:
            DestinationAttribute.objects.bulk_create(attributes_to_be_created, batch_size=50)

        if attributes_to_be_updated:
            DestinationAttribute.objects.bulk_update(
                attributes_to_be_updated, fields=['detail', 'value', 'active', 'is_failure_email_sent', 'updated_at',], batch_size=50)

class ExpenseAttribute(models.Model):
    """
    Fyle Expense Attributes
    """
    id = models.AutoField(primary_key=True)
    org = models.ForeignKey(Org, on_delete=models.PROTECT, help_text='Reference to Org model')
    attribute_type = models.CharField(max_length=255, help_text='Type of expense attribute')
    value = models.CharField(max_length=255, help_text='Value of expense attribute')
    active = models.BooleanField(null=True, help_text='Indicates whether the fields is active or not')
    detail = JSONField(help_text='Detailed expense attributes payload', null=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at datetime')
    source_id = models.CharField(max_length=255, help_text='Fyle ID')
    auto_created = models.BooleanField(default=False,
                                    help_text='Indicates whether the field is auto created by the integration')

    class Meta:
        db_table = 'expense_attributes'
        unique_together = ('value', 'attribute_type', 'org')

    @staticmethod
    def create_or_update_expense_attribute(attribute: Dict, org_id):
        """
        Get or create expense attribute
        """
        expense_attribute, _ = ExpenseAttribute.objects.update_or_create(
            attribute_type=attribute['attribute_type'],
            value=attribute['value'],
            org_id=org_id,
            defaults={
                'active': attribute['active'] if 'active' in attribute else None,
                'source_id': attribute['source_id'],
                'detail': attribute['detail'] if 'detail' in attribute else None
            }
        )
        return expense_attribute

    @staticmethod
    def bulk_create_or_update_expense_attributes(
            attributes: List[Dict], attribute_type: str, org_id: int, update: bool = False):
        """
        Create Expense Attributes in bulk
        :param update: Update Pre-existing records or not
        :param attribute_type: Attribute type
        :param attributes: attributes = [{
            'attribute_type': Type of attribute,
            'value': Value of attribute,
            'source_id': Fyle Id of the attribute,
            'detail': Extra Details of the attribute
        }]
        :param org_id: Org Id
        :return: created / updated attributes
        """
        attribute_value_list = [attribute['value'] for attribute in attributes]

        existing_attributes = ExpenseAttribute.objects.filter(
            value__in=attribute_value_list, attribute_type=attribute_type,
            org_id=org_id).values('id', 'detail', 'value', 'active')

        existing_attribute_values = []

        primary_key_map = {}

        for existing_attribute in existing_attributes:
            existing_attribute_values.append(existing_attribute['value'])
            primary_key_map[existing_attribute['value']] = {
                'id': existing_attribute['id'],
                'detail': existing_attribute['detail'],
                'active': existing_attribute['active']
            }

        attributes_to_be_created = []
        attributes_to_be_updated = []

        values_appended = []
        for attribute in attributes:
            if attribute['value'] not in existing_attribute_values and attribute['value'] not in values_appended:
                values_appended.append(attribute['value'])
                attributes_to_be_created.append(
                    ExpenseAttribute(
                        attribute_type=attribute_type,
                        value=attribute['value'],
                        source_id=attribute['source_id'],
                        detail=attribute['detail'] if 'detail' in attribute else None,
                        org_id=org_id,
                        active=attribute['active'] if 'active' in attribute else None
                    )
                )
            else:
                if update:
                    attributes_to_be_updated.append(
                        ExpenseAttribute(
                            id=primary_key_map[attribute['value']]['id'],
                            source_id=attribute['source_id'],
                            detail=attribute['detail'] if 'detail' in attribute else None,
                            active=attribute['active'] if 'active' in attribute else None
                        )
                    )
        if attributes_to_be_created:
            ExpenseAttribute.objects.bulk_create(attributes_to_be_created, batch_size=50)

        if attributes_to_be_updated:
            ExpenseAttribute.objects.bulk_update(
                attributes_to_be_updated, fields=['source_id', 'detail', 'active'], batch_size=50)


class Mapping(models.Model):
    """
    Mappings
    """
    id = models.AutoField(primary_key=True)
    source_type = models.CharField(max_length=255, help_text='Fyle Enum')
    destination_type = models.CharField(max_length=255, help_text='Destination Enum')
    source = models.ForeignKey(ExpenseAttribute, on_delete=models.PROTECT, related_name='mapping')
    destination = models.ForeignKey(DestinationAttribute, on_delete=models.PROTECT, related_name='mapping')
    org = models.ForeignKey(Org, on_delete=models.PROTECT, help_text='Reference to Org model')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at datetime')

    class Meta:
        db_table = 'mappings'

    @staticmethod
    def create_or_update_mapping(source_type: str, destination_type: str, source_value: str, 
        destination_value: str, destination_id: str, org_id: int):
        """
        Bulk update or create mappings
        source_type = 'Type of Source attribute, eg. CATEGORY',
        destination_type = 'Type of Destination attribute, eg. ACCOUNT',
        source_value = 'Source value to be mapped, eg. category name',
        destination_value = 'Destination value to be mapped, eg. account name'
        workspace_id = Unique Workspace id
        """

        mapping, _ = Mapping.objects.update_or_create(
            source_type=source_type,
            source=ExpenseAttribute.objects.filter(
                attribute_type=source_type, value__iexact=source_value, org_id=org_id
            ).first() if source_value else None,
            destination_type=destination_type,
            org=Org.objects.get(pk=org_id),
            defaults={
                'destination': DestinationAttribute.objects.get(
                    attribute_type=destination_type,
                    value=destination_value,
                    destination_id=destination_id,
                    org_id=org_id
                )
            }
        )

        return mapping