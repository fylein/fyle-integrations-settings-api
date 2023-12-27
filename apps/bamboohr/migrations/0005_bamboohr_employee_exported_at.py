# Generated by Django 3.1.14 on 2023-12-26 16:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bamboohr', '0004_auto_20221220_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='bamboohr',
            name='employee_exported_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Employee exported to Fyle at datetime'),
            preserve_default=False,
        ),
    ]