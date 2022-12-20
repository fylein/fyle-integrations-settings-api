# Generated by Django 3.1.14 on 2022-12-19 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0002_remove_org_is_bamboo_connector'),
        ('bamboohr', '0002_configuration'),
    ]

    operations = [
        migrations.CreateModel(
            name='BambooHrConfiguration',
            fields=[
                ('id', models.AutoField(help_text='Unique Id to indentify a Configuration', primary_key=True, serialize=False)),
                ('recipe_id', models.CharField(help_text='Recipe Id', max_length=255, null=True)),
                ('recipe_data', models.TextField(help_text='Code For Recipe', null=True)),
                ('recipe_status', models.BooleanField(help_text='recipe status', null=True)),
                ('additional_email_options', models.JSONField(default=list, help_text='Email and Name of person to send email', null=True)),
                ('emails_selected', models.JSONField(default=list, help_text='Emails Selected For Email Notification', null=True)),
                ('org', models.OneToOneField(help_text='Reference to Org Table', on_delete=django.db.models.deletion.PROTECT, to='orgs.org')),
            ],
            options={
                'db_table': 'bamboohr_configurations',
            },
        ),
        migrations.DeleteModel(
            name='Configuration',
        ),
    ]
