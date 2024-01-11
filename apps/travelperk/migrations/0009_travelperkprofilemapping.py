# Generated by Django 3.1.14 on 2024-01-11 20:57

import apps.travelperk.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0004_auto_20230627_1133'),
        ('travelperk', '0008_auto_20240102_0517'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelperkProfileMapping',
            fields=[
                ('id', models.AutoField(help_text='Unique Id to indentify a Profile Mapping', primary_key=True, serialize=False)),
                ('profile_name', models.CharField(help_text='Profile Name', max_length=255)),
                ('user_role', models.CharField(choices=[('TRAVELLER', 'TRAVERLLER'), ('BOOKER', 'BOOKER'), ('CARD_HOLDER', 'CARD_HOLDER')], default=apps.travelperk.models.get_default_user_role, help_text='User Role', max_length=255, null=True)),
                ('is_import_enabled', models.BooleanField(default=False, help_text='If Import Is Enabled')),
                ('country', models.CharField(help_text='Country of the payment profile', max_length=255, null=True)),
                ('currency', models.CharField(help_text='Currency of the payment profile', max_length=100, null=True)),
                ('source_id', models.CharField(help_text='Source Id of the payment profile', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at datetime')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at datetime')),
                ('org', models.ForeignKey(help_text='Reference to Org Table', on_delete=django.db.models.deletion.PROTECT, to='orgs.org')),
            ],
            options={
                'db_table': 'travelperk_profile_mappings',
            },
        ),
    ]
