# Generated by Django
from django.db import migrations
from apps.internal.helpers import safe_run_sql

sql_files = [
    'fyle-integrations-db-migrations/integrations_settings/functions/ws_org_id.sql',
    'fyle-integrations-db-migrations/integrations_settings/functions/ws_search.sql',
    'fyle-integrations-db-migrations/integrations_settings/functions/ws_email.sql',
    
    'fyle-integrations-db-migrations/common/global_shared/helpers/add-replication-identity.sql',
    'fyle-integrations-db-migrations/integrations_settings/helpers/add-tables-to-publication.sql'
]


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('orgs', '0008_auto_20250114_1521')
    ]
    operations = safe_run_sql(sql_files)
