# Generated by Django 3.1.14 on 2024-02-01 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelperk', '0011_travelperkadvancedsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelperk',
            name='onboarding_state',
            field=models.CharField(choices=[('CONNECTION', 'CONNECTION'), ('IMPORT_SETTINGS', 'IMPORT_SETTINGS'), ('ADVANCED_SETTINGS', 'ADVANCED_SETTINGS')], default='CONNECTION', help_text='Onboarding State', max_length=255),
        ),
    ]
