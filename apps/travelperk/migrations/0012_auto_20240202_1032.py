# Generated by Django 3.1.14 on 2024-02-02 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travelperk', '0011_travelperkadvancedsetting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelperk',
            name='folder_id',
        ),
        migrations.RemoveField(
            model_name='travelperk',
            name='is_s3_connected',
        ),
        migrations.RemoveField(
            model_name='travelperk',
            name='is_travelperk_connected',
        ),
        migrations.RemoveField(
            model_name='travelperk',
            name='package_id',
        ),
        migrations.RemoveField(
            model_name='travelperk',
            name='travelperk_connection_id',
        ),
        migrations.RemoveField(
            model_name='travelperkconfiguration',
            name='is_recipe_enabled',
        ),
        migrations.RemoveField(
            model_name='travelperkconfiguration',
            name='recipe_data',
        ),
        migrations.RemoveField(
            model_name='travelperkconfiguration',
            name='recipe_id',
        ),
    ]
