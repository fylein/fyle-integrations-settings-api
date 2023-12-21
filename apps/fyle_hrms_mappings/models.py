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
                'display_name': attribute['display_name'],
                'value': attribute['value'],
                'detail': attribute['detail'] if 'detail' in attribute else None
            }
        )
        return destination_attribute
    
    @staticmethod
    def bulk_create_or_update_destination_attributes(
            attributes: List[Dict], attribute_type: str, org_id: int, update: bool = False, display_name: str = None):
        """
        Create Destination Attributes in bulk
        :param update: Update Pre-existing records or not
        :param attribute_type: Attribute type
        :param attributes: attributes = [{
            'attribute_type': Type of attribute,
            'display_name': Display_name of attribute_field,
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
        if display_name:
            filters['display_name'] = display_name

        existing_attributes = DestinationAttribute.objects.filter(**filters)\
            .values('id', 'destination_id', 'detail', 'active')

        existing_attribute_destination_ids = []

        primary_key_map = {}

        for existing_attribute in existing_attributes:
            existing_attribute_destination_ids.append(existing_attribute['destination_id'])
            primary_key_map[existing_attribute['destination_id']] = {
                'id': existing_attribute['id'],
                'value': existing_attribute['value'],
                'detail': existing_attribute['detail'],
                'active' : existing_attribute['active']
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
                        display_name=attribute['display_name'],
                        value=attribute['value'],
                        destination_id=attribute['destination_id'],
                        detail=attribute['detail'] if 'detail' in attribute else None,
                        org_id=org_id,
                        active=attribute['active'] if 'active' in attribute else None
                    )
                )
            else:
                if update and (
                        (attribute['value'] != primary_key_map[attribute['destination_id']]['value'])
                        or
                        ('detail' in attribute and attribute['detail'] != primary_key_map[attribute['destination_id']]['detail'])
                        or
                        ('active' in attribute and attribute['active'] != primary_key_map[attribute['destination_id']]['active'])
                    ):
                    attributes_to_be_updated.append(
                        DestinationAttribute(
                            id=primary_key_map[attribute['destination_id']]['id'],
                            value=attribute['value'],
                            detail=attribute['detail'] if 'detail' in attribute else None,
                            active=attribute['active'] if 'active' in attribute else None,
                            updated_at=datetime.now()
                        )
                    )
        if attributes_to_be_created:
            DestinationAttribute.objects.bulk_create(attributes_to_be_created, batch_size=50)

        if attributes_to_be_updated:
            DestinationAttribute.objects.bulk_update(
                attributes_to_be_updated, fields=['detail', 'value', 'active', 'updated_at'], batch_size=50)

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
                'display_name': attribute['display_name'],
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
            'display_name': Display_name of attribute_field,
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
            org_id=org_id).values('id', 'detail', 'active')

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
                        display_name=attribute['display_name'],
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
