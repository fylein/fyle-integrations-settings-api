import pytest
from django.db import IntegrityError
from apps.fyle_hrms_mappings.models import DestinationAttribute, ExpenseAttribute, Mapping
from apps.orgs.models import Org


def test_destination_attribute_creation(db, add_org):
    """
    Test DestinationAttribute model creation
    """
    attribute_data = {
        'attribute_type': 'DEPARTMENT',
        'value': 'Engineering',
        'destination_id': 'dept_123',
        'active': True,
        'detail': {'code': 'ENG', 'description': 'Engineering Department'}
    }
    
    destination_attribute = DestinationAttribute.objects.create(
        org=add_org,
        **attribute_data
    )
    
    assert destination_attribute.attribute_type == 'DEPARTMENT'
    assert destination_attribute.value == 'Engineering'
    assert destination_attribute.destination_id == 'dept_123'
    assert destination_attribute.active is True
    assert destination_attribute.detail == {'code': 'ENG', 'description': 'Engineering Department'}
    assert destination_attribute.auto_created is False
    assert destination_attribute.is_failure_email_sent is False
    assert destination_attribute.org == add_org


def test_destination_attribute_unique_constraint(db, add_org):
    """
    Test DestinationAttribute unique constraint on (destination_id, attribute_type, org)
    """
    # Create first attribute
    DestinationAttribute.objects.create(
        org=add_org,
        attribute_type='DEPARTMENT',
        value='Engineering',
        destination_id='dept_123'
    )
    
    # Try to create duplicate - should raise IntegrityError
    with pytest.raises(IntegrityError):
        DestinationAttribute.objects.create(
            org=add_org,
            attribute_type='DEPARTMENT',
            value='Different Value',
            destination_id='dept_123'
        )


def test_destination_attribute_create_or_update_method(db, add_org):
    """
    Test DestinationAttribute.create_or_update_destination_attribute method
    """
    # Test creation
    attribute_data = {
        'attribute_type': 'DEPARTMENT',
        'value': 'Engineering',
        'destination_id': 'dept_123',
        'active': True,
        'detail': {'code': 'ENG'}
    }
    
    destination_attribute = DestinationAttribute.create_or_update_destination_attribute(
        attribute_data, add_org.id
    )
    
    assert destination_attribute.attribute_type == 'DEPARTMENT'
    assert destination_attribute.value == 'Engineering'
    assert destination_attribute.destination_id == 'dept_123'
    
    # Test update
    updated_attribute_data = {
        'attribute_type': 'DEPARTMENT',
        'value': 'Engineering Updated',
        'destination_id': 'dept_123',
        'active': False,
        'detail': {'code': 'ENG_UPDATED'}
    }
    
    updated_attribute = DestinationAttribute.create_or_update_destination_attribute(
        updated_attribute_data, add_org.id
    )
    
    assert updated_attribute.id == destination_attribute.id
    assert updated_attribute.value == 'Engineering Updated'
    assert updated_attribute.active is False
    assert updated_attribute.detail == {'code': 'ENG_UPDATED'}


def test_destination_attribute_bulk_create_or_update_method(db, add_org):
    """
    Test DestinationAttribute.bulk_create_or_update_destination_attributes method
    """
    attributes = [
        {
            'attribute_type': 'DEPARTMENT',
            'value': 'Engineering',
            'destination_id': 'dept_123',
            'active': True,
            'detail': {'code': 'ENG'}
        },
        {
            'attribute_type': 'DEPARTMENT',
            'value': 'Marketing',
            'destination_id': 'dept_456',
            'active': True,
            'detail': {'code': 'MKT'}
        }
    ]
    
    # Test bulk creation
    DestinationAttribute.bulk_create_or_update_destination_attributes(
        attributes, 'DEPARTMENT', add_org.id
    )
    
    created_attributes = DestinationAttribute.objects.filter(
        org=add_org, attribute_type='DEPARTMENT'
    )
    assert created_attributes.count() == 2
    
    # Test bulk update
    updated_attributes = [
        {
            'attribute_type': 'DEPARTMENT',
            'value': 'Engineering Updated',
            'destination_id': 'dept_123',
            'active': False,
            'detail': {'code': 'ENG_UPDATED'}
        }
    ]
    
    DestinationAttribute.bulk_create_or_update_destination_attributes(
        updated_attributes, 'DEPARTMENT', add_org.id, update=True
    )
    
    updated_attribute = DestinationAttribute.objects.get(destination_id='dept_123')
    assert updated_attribute.value == 'Engineering Updated'
    assert updated_attribute.active is False


def test_expense_attribute_creation(db, add_org):
    """
    Test ExpenseAttribute model creation
    """
    attribute_data = {
        'attribute_type': 'CATEGORY',
        'value': 'Travel',
        'source_id': 'cat_123',
        'active': True,
        'detail': {'code': 'TRV', 'description': 'Travel Expenses'}
    }
    
    expense_attribute = ExpenseAttribute.objects.create(
        org=add_org,
        **attribute_data
    )
    
    assert expense_attribute.attribute_type == 'CATEGORY'
    assert expense_attribute.value == 'Travel'
    assert expense_attribute.source_id == 'cat_123'
    assert expense_attribute.active is True
    assert expense_attribute.detail == {'code': 'TRV', 'description': 'Travel Expenses'}
    assert expense_attribute.auto_created is False
    assert expense_attribute.org == add_org


def test_expense_attribute_unique_constraint(db, add_org):
    """
    Test ExpenseAttribute unique constraint on (value, attribute_type, org)
    """
    # Create first attribute
    ExpenseAttribute.objects.create(
        org=add_org,
        attribute_type='CATEGORY',
        value='Travel',
        source_id='cat_123'
    )
    
    # Try to create duplicate - should raise IntegrityError
    with pytest.raises(IntegrityError):
        ExpenseAttribute.objects.create(
            org=add_org,
            attribute_type='CATEGORY',
            value='Travel',
            source_id='cat_456'
        )


def test_expense_attribute_create_or_update_method(db, add_org):
    """
    Test ExpenseAttribute.create_or_update_expense_attribute method
    """
    # Test creation
    attribute_data = {
        'attribute_type': 'CATEGORY',
        'value': 'Travel',
        'source_id': 'cat_123',
        'active': True,
        'detail': {'code': 'TRV'}
    }
    
    expense_attribute = ExpenseAttribute.create_or_update_expense_attribute(
        attribute_data, add_org.id
    )
    
    assert expense_attribute.attribute_type == 'CATEGORY'
    assert expense_attribute.value == 'Travel'
    assert expense_attribute.source_id == 'cat_123'
    
    # Test update
    updated_attribute_data = {
        'attribute_type': 'CATEGORY',
        'value': 'Travel',
        'source_id': 'cat_123_updated',
        'active': False,
        'detail': {'code': 'TRV_UPDATED'}
    }
    
    updated_attribute = ExpenseAttribute.create_or_update_expense_attribute(
        updated_attribute_data, add_org.id
    )
    
    assert updated_attribute.id == expense_attribute.id
    assert updated_attribute.source_id == 'cat_123_updated'
    assert updated_attribute.active is False
    assert updated_attribute.detail == {'code': 'TRV_UPDATED'}


def test_expense_attribute_bulk_create_or_update_method(db, add_org):
    """
    Test ExpenseAttribute.bulk_create_or_update_expense_attributes method
    """
    attributes = [
        {
            'attribute_type': 'CATEGORY',
            'value': 'Travel',
            'source_id': 'cat_123',
            'active': True,
            'detail': {'code': 'TRV'}
        },
        {
            'attribute_type': 'CATEGORY',
            'value': 'Food',
            'source_id': 'cat_456',
            'active': True,
            'detail': {'code': 'FOOD'}
        }
    ]
    
    # Test bulk creation
    ExpenseAttribute.bulk_create_or_update_expense_attributes(
        attributes, 'CATEGORY', add_org.id
    )
    
    created_attributes = ExpenseAttribute.objects.filter(
        org=add_org, attribute_type='CATEGORY'
    )
    assert created_attributes.count() == 2
    
    # Test bulk update
    updated_attributes = [
        {
            'attribute_type': 'CATEGORY',
            'value': 'Travel',
            'source_id': 'cat_123_updated',
            'active': False,
            'detail': {'code': 'TRV_UPDATED'}
        }
    ]
    
    ExpenseAttribute.bulk_create_or_update_expense_attributes(
        updated_attributes, 'CATEGORY', add_org.id, update=True
    )
    
    updated_attribute = ExpenseAttribute.objects.get(value='Travel')
    assert updated_attribute.source_id == 'cat_123_updated'
    assert updated_attribute.active is False


def test_mapping_creation(db, add_org):
    """
    Test Mapping model creation
    """
    # Create source and destination attributes first
    source_attribute = ExpenseAttribute.objects.create(
        org=add_org,
        attribute_type='CATEGORY',
        value='Travel',
        source_id='cat_123'
    )
    
    destination_attribute = DestinationAttribute.objects.create(
        org=add_org,
        attribute_type='ACCOUNT',
        value='Travel Account',
        destination_id='acc_123'
    )
    
    mapping = Mapping.objects.create(
        source_type='CATEGORY',
        destination_type='ACCOUNT',
        source=source_attribute,
        destination=destination_attribute,
        org=add_org
    )
    
    assert mapping.source_type == 'CATEGORY'
    assert mapping.destination_type == 'ACCOUNT'
    assert mapping.source == source_attribute
    assert mapping.destination == destination_attribute
    assert mapping.org == add_org


def test_mapping_create_or_update_method(db, add_org):
    """
    Test Mapping.create_or_update_mapping method
    """
    # Create source and destination attributes first
    source_attribute = ExpenseAttribute.objects.create(
        org=add_org,
        attribute_type='CATEGORY',
        value='Travel',
        source_id='cat_123'
    )
    
    destination_attribute = DestinationAttribute.objects.create(
        org=add_org,
        attribute_type='ACCOUNT',
        value='Travel Account',
        destination_id='acc_123'
    )
    
    # Test creation
    mapping = Mapping.create_or_update_mapping(
        source_type='CATEGORY',
        destination_type='ACCOUNT',
        source_value='Travel',
        destination_value='Travel Account',
        destination_id='acc_123',
        org_id=add_org.id
    )
    
    assert mapping.source_type == 'CATEGORY'
    assert mapping.destination_type == 'ACCOUNT'
    assert mapping.source == source_attribute
    assert mapping.destination == destination_attribute
    
    # Update the existing destination attribute instead of creating a new one
    destination_attribute.value = 'Travel Account Updated'
    destination_attribute.save()
    
    # Test update (should return same mapping but with updated destination)
    updated_mapping = Mapping.create_or_update_mapping(
        source_type='CATEGORY',
        destination_type='ACCOUNT',
        source_value='Travel',
        destination_value='Travel Account Updated',
        destination_id='acc_123',
        org_id=add_org.id
    )
    
    assert updated_mapping.id == mapping.id
    # The destination should be updated to the new destination attribute
    assert updated_mapping.destination.value == 'Travel Account Updated'


def test_mapping_with_none_source_value(db, add_org):
    """
    Test Mapping.create_or_update_mapping method with None source_value
    Note: This test shows that the current implementation has issues with None source_value
    """
    destination_attribute = DestinationAttribute.objects.create(
        org=add_org,
        attribute_type='ACCOUNT',
        value='Travel Account',
        destination_id='acc_123'
    )
    
    # The current implementation has issues with None source_value
    # The source field is not nullable but the method tries to set it to None
    # This test documents the current behavior
    with pytest.raises(Exception):
        mapping = Mapping.create_or_update_mapping(
            source_type='CATEGORY',
            destination_type='ACCOUNT',
            source_value=None,
            destination_value='Travel Account',
            destination_id='acc_123',
            org_id=add_org.id
        )


def test_model_relationships(db, add_org):
    """
    Test relationships between models
    """
    # Create attributes
    source_attribute = ExpenseAttribute.objects.create(
        org=add_org,
        attribute_type='CATEGORY',
        value='Travel',
        source_id='cat_123'
    )
    
    destination_attribute = DestinationAttribute.objects.create(
        org=add_org,
        attribute_type='ACCOUNT',
        value='Travel Account',
        destination_id='acc_123'
    )
    
    # Create mapping
    mapping = Mapping.objects.create(
        source_type='CATEGORY',
        destination_type='ACCOUNT',
        source=source_attribute,
        destination=destination_attribute,
        org=add_org
    )
    
    # Test relationships
    assert mapping.source == source_attribute
    assert mapping.destination == destination_attribute
    assert mapping.org == add_org
    
    # Test reverse relationships
    assert source_attribute.mapping.first() == mapping
    assert destination_attribute.mapping.first() == mapping 
 