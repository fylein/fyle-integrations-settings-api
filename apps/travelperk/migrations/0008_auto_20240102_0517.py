# Generated by Django 3.1.14 on 2024-01-02 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0004_auto_20230627_1133'),
        ('travelperk', '0007_auto_20231219_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='pdf',
            field=models.TextField(help_text='URL to the PDF version of the invoice.'),
        ),
        migrations.CreateModel(
            name='ImportedExpenseDetail',
            fields=[
                ('id', models.AutoField(help_text='Unique Id to indentify a Imported Expense Detail', primary_key=True, serialize=False)),
                ('expense_id', models.CharField(help_text='Expense Id', max_length=255)),
                ('file_id', models.CharField(help_text='File Id', max_length=255, null=True)),
                ('is_reciept_attached', models.BooleanField(default=False, help_text='If Reciept Is Attached')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Created at datetime')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated at datetime')),
                ('org', models.ForeignKey(help_text='Reference to Org Table', on_delete=django.db.models.deletion.PROTECT, to='orgs.org')),
            ],
            options={
                'db_table': 'imported_expense_details',
            },
        ),
    ]