# Generated by Django 3.1.14 on 2023-03-13 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travelperk', '0002_travelperk_travelperk_connection_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelperk',
            name='is_fyle_connected',
        ),
    ]