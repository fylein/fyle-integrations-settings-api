# Generated by Django 3.1.14 on 2024-04-19 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelperk', '0014_auto_20240212_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='reference',
            field=models.CharField(help_text='Reference information for the invoice (e.g., Trip #9876543).', max_length=255),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='travelperk_bank_account',
            field=models.CharField(blank=True, help_text='TravelPerk bank account information if available.', max_length=255, null=True),
        ),
    ]
