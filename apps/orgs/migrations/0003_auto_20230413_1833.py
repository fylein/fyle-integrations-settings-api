# Generated by Django 3.1.14 on 2023-04-13 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0002_auto_20221219_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='allow_gusto',
            field=models.BooleanField(default=False, help_text='Allow Gusto'),
        ),
        migrations.AddField(
            model_name='org',
            name='allow_travelperk',
            field=models.BooleanField(default=False, help_text='Allow Travelperk'),
        ),
    ]