# Generated by Django 3.1.14 on 2023-01-12 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orgs', '0002_auto_20221219_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelPerkConfiguration',
            fields=[
                ('id', models.AutoField(help_text='Unique Id to indentify a Configuration', primary_key=True, serialize=False)),
                ('recipe_id', models.CharField(help_text='Recipe Id', max_length=255, null=True)),
                ('recipe_data', models.TextField(help_text='Code For Recipe', null=True)),
                ('recipe_status', models.BooleanField(help_text='recipe status', null=True)),
                ('org', models.OneToOneField(help_text='Reference to Org Table', on_delete=django.db.models.deletion.PROTECT, to='orgs.org')),
            ],
            options={
                'db_table': 'travelperk_configurations',
            },
        ),
        migrations.CreateModel(
            name='TravelPerk',
            fields=[
                ('id', models.AutoField(help_text='Unique Id to indentify a Org', primary_key=True, serialize=False)),
                ('folder_id', models.CharField(help_text='Travelperk Folder ID', max_length=255, null=True)),
                ('package_id', models.CharField(help_text='Travelperk Package ID', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at datetime')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at datetime')),
                ('org', models.OneToOneField(help_text='Reference to Org table', on_delete=django.db.models.deletion.PROTECT, to='orgs.org')),
            ],
            options={
                'db_table': 'travelperk',
            },
        ),
    ]
