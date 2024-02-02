from typing import Dict, List

from django.db import models, transaction
from django.contrib.postgres.fields import ArrayField

from apps.orgs.models import Org


LINEITEM_STRUCTURE_CHOICE = (
    ('MULTIPLE', 'MULTIPLE'),
    ('SINGLE', 'SINGLE'),
)

USER_ROLE_CHOICES = (
    ('TRAVELLER', 'TRAVELLER'),
    ('BOOKER', 'BOOKER'),
    ('CARD_HOLDER', 'CARD_HOLDER')
)


class TravelperkCredential(models.Model):
    """
    Travelperk Credential Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Credentials')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org table')
    refresh_token = models.CharField(max_length=255, null=True, help_text='Travelperk Refresh Token')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at =  models.DateTimeField(auto_now=True, help_text='Updated at datetime')
    
    class Meta:
        db_table = 'travelperk_credentials'


class Invoice(models.Model):
    """
    Travelperk Invoice Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique identifier for the invoice.')
    billing_information = models.JSONField(help_text='Billing information associated with the invoice.')
    billing_period = models.CharField(max_length=20, help_text='Billing period type (e.g., instant).')
    currency = models.CharField(max_length=3, help_text='Currency code (e.g., GBP).')
    org_id = models.ForeignKey(Org, on_delete=models.CASCADE, help_text='Reference to Org table')
    due_date = models.DateField(help_text='Due date for the invoice.')
    from_date = models.DateField(help_text='Start date for the billing period.')
    to_date = models.DateField(help_text='End date for the billing period.')
    issuing_date = models.DateField(help_text='Date when the invoice was issued.')

    mode = models.CharField(
        max_length=20,
        choices=[('reseller', 'Reseller'), ('direct', 'Direct')],
        help_text='Mode of the invoice, indicating whether it is a reseller or direct invoice.'
    )
    pdf = models.TextField(help_text='URL to the PDF version of the invoice.')
    profile_id = models.CharField(max_length=255, help_text='ID of the profile associated with the invoice.')
    profile_name = models.CharField(max_length=255, help_text='Name of the profile associated with the invoice.')
    reference = models.CharField(max_length=50, help_text='Reference information for the invoice (e.g., Trip #9876543).')
    serial_number = models.CharField(max_length=20, help_text='Serial number of the invoice.')
    status = models.CharField(max_length=20, help_text='Status of the invoice (e.g., paid).')
    taxes_summary = models.JSONField(help_text='Summary of taxes applied to the invoice.')
    total = models.DecimalField(max_digits=10, decimal_places=2, help_text='Total amount of the invoice.')
    travelperk_bank_account = models.CharField(max_length=50, null=True, blank=True, help_text='TravelPerk bank account information if available.')

    exported_to_fyle = models.BooleanField(default=False, help_text='If the invoice is exported to Fyle')


    class Meta:
        db_table = 'invoices'
        
    @staticmethod
    def create_or_update_invoices(invoice_data, org_id):
        """
        Create or update invoice object
        """

        # Create or update Invoice object based on serial_number
        invoice_object, _ = Invoice.objects.update_or_create(
            serial_number=invoice_data['serial_number'],
            org_id_id=org_id,
            defaults={
                'billing_information': invoice_data['billing_information'],
                'billing_period': invoice_data['billing_period'],
                'currency': invoice_data['currency'],
                'due_date': invoice_data['due_date'],
                'from_date': invoice_data['from_date'],
                'to_date': invoice_data['to_date'],
                'issuing_date': invoice_data['issuing_date'],
                'mode': invoice_data['mode'],
                'pdf': invoice_data['pdf'],
                'profile_id': invoice_data['profile_id'],
                'profile_name': invoice_data['profile_name'],
                'reference': invoice_data['reference'],
                'status': invoice_data['status'],
                'taxes_summary': invoice_data['taxes_summary'],
                'total': invoice_data['total'],
                'travelperk_bank_account': invoice_data['travelperk_bank_account'],
                'exported_to_fyle': False,
            }
        )

        return invoice_object


class InvoiceLineItem(models.Model):
    """
    Travelperk Invoice Line Item Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique identifier for the line item.')
    invoice_line_id = models.CharField(max_length=255, help_text='id for invoice line')
    expense_date = models.DateField(help_text='Date of the expense for this line item.')
    description = models.CharField(max_length=255, help_text='Description of the product or service.')
    quantity = models.IntegerField(help_text='Quantity of the product or service.')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Unit price of the product or service.')
    non_taxable_unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Non-taxable unit price.')
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text='Tax percentage applied.')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Total tax amount for this line item.')
    tax_regime = models.CharField(max_length=20, help_text='Tax regime for this line item.')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Total amount including taxes.')

    # Metadata
    trip_id = models.CharField(max_length=255, help_text='ID of the trip associated with this line item.')
    trip_name = models.CharField(max_length=255, help_text='Name of the trip associated with this line item.')
    service = models.CharField(max_length=50, help_text='Type of service (e.g., PREMIUM).')

    # Booker
    booker_name = models.CharField(max_length=100, help_text='Name of the person who booked the service.')
    booker_email = models.EmailField(help_text='Email address of the person who booked the service.')
    
    # Cost Center
    cost_center = models.CharField(max_length=20, help_text='Cost center associated with this line item.')
    vendor = models.CharField(max_length=255, null=True, help_text='Vendor name.')

    # Other Fields
    credit_card_last_4_digits = models.CharField(max_length=4, help_text='Last 4 digits of the credit card used for payment.')

    # Foreign Key to Invoice
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='line_items', help_text='Invoice associated with this line item.')

    class Meta:
        db_table = 'invoice_line_items'

    @staticmethod
    def create_or_update_invoice_lineitems(invoice_lineitems_data, invoice_id):
        """
        Create or update invoice line item object
        """
        
        invoice_lineitems_objects = []
        for line_item_data in invoice_lineitems_data:
            invoice_linteitem, _ = InvoiceLineItem.objects.update_or_create(
                invoice_line_id=line_item_data['id'],
                defaults={
                    'expense_date': line_item_data['expense_date'],
                    'description': line_item_data['description'],
                    'quantity': line_item_data['quantity'],
                    'unit_price': line_item_data['unit_price'],
                    'non_taxable_unit_price': line_item_data['non_taxable_unit_price'],
                    'tax_percentage': line_item_data['tax_percentage'],
                    'tax_amount': line_item_data['tax_amount'],
                    'tax_regime': line_item_data['tax_regime'],
                    'total_amount': line_item_data['total_amount'],
                    'trip_id': line_item_data['metadata']['trip_id'],
                    'trip_name': line_item_data['metadata']['trip_name'],
                    'service': line_item_data['metadata']['service'],
                    'booker_name': line_item_data['metadata']['booker']['name'],
                    'booker_email': line_item_data['metadata']['booker']['email'],
                    'cost_center': line_item_data['metadata']['cost_center'],
                    'vendor': line_item_data['metadata']['vendor'],
                    'credit_card_last_4_digits': line_item_data['metadata']['credit_card_last_4_digits'],
                    'invoice': invoice_id,
                }
            )
            invoice_lineitems_objects.append(invoice_linteitem)

        return invoice_lineitems_objects


class TravelPerk(models.Model):
    """
    Travelperk Model
    """
    
    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Org')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org table')
    webhook_subscription_id = models.CharField(max_length=255, null=True, help_text='Webhook Subscription Id')
    webhook_enabled = models.BooleanField(null=True, help_text='If Webhook Is Enabled')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at =  models.DateTimeField(auto_now=True, help_text='Updated at datetime')

    class Meta:
       db_table = 'travelperk'


class TravelPerkConfiguration(models.Model):
    """
    TravelperkConfiguration Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Configuration')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org Table')

    class Meta:
        db_table = 'travelperk_configurations'


class ImportedExpenseDetail(models.Model):
    """
    Detail of imported expense
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Imported Expense Detail')
    org = models.ForeignKey(Org, on_delete=models.PROTECT, help_text='Reference to Org Table')
    expense_id = models.CharField(max_length=255, help_text='Expense Id')
    file_id = models.CharField(null=True, max_length=255, help_text='File Id')
    is_reciept_attached = models.BooleanField(default=False, help_text='If Reciept Is Attached')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at =  models.DateTimeField(auto_now=True, help_text='Updated at datetime')

    class Meta:
        db_table = 'imported_expense_details'


class TravelperkAdvancedSetting(models.Model):
    """
    Advance Settings for travelperk
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Advance Settings')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org Table')
    default_employee_name = models.CharField(max_length=255, null=True, help_text='Default Employee Name')
    default_employee_id = models.CharField(max_length=255, null=True, help_text='Default Employee Id')
    default_category_name = models.CharField(max_length=255, null=True, help_text='Default Category Name')
    default_category_id = models.CharField(max_length=255, null=True, help_text='Default Category Id')
    invoice_lineitem_structure = models.CharField(choices=LINEITEM_STRUCTURE_CHOICE, default='MULTIPLE', max_length=255, help_text='Invoice Lineitem Structure')
    description_structure = ArrayField(
        models.CharField(max_length=255), help_text='Array of fields in memo', null=True
    )
    emails_added = models.JSONField(default=list, null=True, help_text='Emails Selected For Email Notification')
    created_at = models.DateField(auto_now_add=True, help_text='Created at datetime')
    updated_at = models.DateField(auto_now=True, help_text='Updated at datetime')

    class Meta:
        db_table = 'travelperk_advanced_settings'


class TravelperkProfileMapping(models.Model):
    """
    Detail of profile mapping
    """
    
    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Profile Mapping')
    org = models.ForeignKey(Org, on_delete=models.PROTECT, help_text='Reference to Org Table')
    profile_name = models.CharField(max_length=255, help_text='Profile Name')
    user_role = models.CharField(max_length=255, choices=USER_ROLE_CHOICES, null=True, help_text='User Role')
    is_import_enabled = models.BooleanField(default=False, help_text='If Import Is Enabled')
    country = models.CharField(max_length=255, null=True, help_text='Country of the payment profile')
    currency = models.CharField(max_length=100, null=True, help_text='Currency of the payment profile')
    source_id = models.CharField(max_length=255, help_text='Source Id of the payment profile')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at =  models.DateTimeField(auto_now=True, help_text='Updated at datetime')

    class Meta:
        db_table = 'travelperk_profile_mappings'

    @staticmethod
    def bulk_create_profile_mappings(mappings: List[Dict], org_id: str):
        """
        Bulk update or create profile mappings
        """

        travelperk_profile_mappings = []
        with transaction.atomic():
            for mapping in mappings:
                profile_mappings, _ = TravelperkProfileMapping.objects.update_or_create(
                    org_id=org_id,
                    profile_name=mapping['profile_name'],
                    defaults={
                        'user_role': mapping['user_role'],
                        'is_import_enabled': mapping['is_import_enabled'],
                    }
                )

                travelperk_profile_mappings.append(profile_mappings)

        return travelperk_profile_mappings
