from django.db import migrations
from apps.internal.helpers import safe_run_sql

sql_files = [
    'fyle-integrations-db-migrations/integrations_settings/helpers/add-schedule-to-upload-s3.sql',
]


class Migration(migrations.Migration):
    dependencies = [('integrations', '0005_auto_20240223_1251')]
    operations = safe_run_sql(sql_files)
