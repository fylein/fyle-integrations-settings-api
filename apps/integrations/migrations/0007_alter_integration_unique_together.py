# Generated by Django 4.2.18 on 2025-03-04 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0006_integrations_add_errors_count_token_expired'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='integration',
            unique_together={('org_id', 'type')},
        ),
    ]
