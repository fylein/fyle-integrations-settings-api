# Generated by Django 3.1.14 on 2024-08-01 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0004_auto_20230627_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='allow_dynamics',
            field=models.BooleanField(default=True, help_text='Allow Dynamics'),
        ),
    ]
