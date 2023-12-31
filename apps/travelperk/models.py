from django.db import models

from apps.orgs.models import Org

# Create your models here.

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
    due_date = models.DateField(help_text='Due date for the invoice.')
    from_date = models.DateField(help_text='Start date for the billing period.')
    to_date = models.DateField(help_text='End date for the billing period.')
    issuing_date = models.DateField(help_text='Date when the invoice was issued.')

    mode = models.CharField(
        max_length=20,
        choices=[('reseller', 'Reseller'), ('direct', 'Direct')],
        help_text='Mode of the invoice, indicating whether it is a reseller or direct invoice.'
    )
    pdf = models.URLField(help_text='URL to the PDF version of the invoice.')
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


class InvoiceLineItem(models.Model):
    """
    Travelperk Invoice Line Item Model
    """

    id = models.AutoField(primary_key=True, help_text='Unique identifier for the line item.')
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
    
    # Other Fields
    credit_card_last_4_digits = models.CharField(max_length=4, help_text='Last 4 digits of the credit card used for payment.')
    
    # Foreign Key to Invoice
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='line_items', help_text='Invoice associated with this line item.')

    class Meta:
        db_table = 'invoice_line_items'


class TravelPerk(models.Model):
    """
    Travelperk Model
    """
    
    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Org')
    org = models.OneToOneField(Org, on_delete=models.PROTECT, help_text='Reference to Org table')
    folder_id = models.CharField(max_length=255, null=True, help_text='Travelperk Folder ID')
    package_id = models.CharField(max_length=255, null=True, help_text="Travelperk Package ID")
    is_s3_connected = models.BooleanField(null=True, help_text='If S3 Is Connectoed')
    is_travelperk_connected = models.BooleanField(null=True, help_text='If Travelperk Is Connected')
    travelperk_connection_id = models.IntegerField(null=True, help_text='Travelperk Connection Id')
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
    recipe_id = models.CharField(max_length=255, help_text='Recipe Id', null=True)
    recipe_data = models.TextField(help_text='Code For Recipe', null=True)
    is_recipe_enabled = models.BooleanField(help_text='recipe status', null=True)

    class Meta:
        db_table = 'travelperk_configurations'


class ImportedExpenseDetail(models.Model):
    """
    Detail of imported expense
    """

    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify a Imported Expense Detail')
    org = models.ForeignKey(Org, on_delete=models.PROTECT, help_text='Reference to Org Table')
    expense_id = models.CharField(max_length=255, help_text='Expense Id')
    file_id = models.CharField(max_length=255, help_text='File Id')
    is_reciept_attached = models.BooleanField(help_text='If Reciept Is Attached')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at datetime')
    updated_at =  models.DateTimeField(auto_now=True, help_text='Updated at datetime')
