# Generated by Django 3.1.14 on 2022-12-19 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='org',
            name='is_bamboo_connector',
        ),
        migrations.AddField(
            model_name='org',
            name='is_fyle_connected',
            field=models.BooleanField(help_text='Is Fyle API Connected', null=True),
        ),
        migrations.AddField(
            model_name='org',
            name='is_sendgrid_connected',
            field=models.BooleanField(help_text='Is Sendgrid Connected', null=True),
        ),
    ]