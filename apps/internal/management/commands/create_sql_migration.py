import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from django.db.migrations import loader


class Command(BaseCommand):
    help = 'Generate a migration file for running SQL files'
    def add_arguments(self, parser):
        parser.add_argument(
            'sql_files',
            nargs='+',
            help='Paths to the SQL files to include in the migration',
        )
        parser.add_argument(
            '--app',
            default='internal',
            help='The Django app to create the migration for',
        )
    def get_latest_migration(self, app_name):
        """Get the latest migration name using Django's migration loader."""
        migration_loader = loader.MigrationLoader(None)
        app_migrations = [
            name for app, name in migration_loader.disk_migrations.keys()
            if app == app_name
        ]
        if app_migrations:
            return sorted(app_migrations)[-1]
        return None
    def handle(self, *args, **options):
        app_name = options['app']
        sql_files = options['sql_files']
        validated_sql_files = []
        for file_path in sql_files:
            absolute_path = os.path.join(settings.BASE_DIR, file_path)
            if not os.path.exists(absolute_path):
                self.stderr.write(
                    self.style.ERROR(f"File not found: {file_path} "
                                   f"(looked in {absolute_path})")
                )
                return
            validated_sql_files.append(file_path)
        try:
            app_config = apps.get_app_config(app_name)
            app_path = app_config.path
            migrations_dir = os.path.join(app_path, 'migrations')
        except LookupError:
            self.stderr.write(self.style.ERROR(f"App '{app_name}' not found. Make sure it's in INSTALLED_APPS"))
            return
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
        latest_migration = self.get_latest_migration(app_name)
        if latest_migration:
            dependencies = f"[('{app_name}', '{latest_migration}')]"
        else:
            dependencies = "[]  # This is the first migration"
        existing_migrations = [f for f in os.listdir(migrations_dir) if f.endswith('.py')]
        migration_number = len([f for f in existing_migrations if f != '__init__.py']) + 1
        migration_name = f"{migration_number:04d}_auto_generated_sql.py"
        migration_file_path = os.path.join(migrations_dir, migration_name)
        formatted_sql_files = []
        for file_path in validated_sql_files:
            normalized_path = file_path.replace('\\', '/')
            formatted_sql_files.append(f"'{normalized_path}'")
        sql_files_str = ',\n    '.join(formatted_sql_files)
        migration_content = f"""# Generated by Django
from django.db import migrations
from apps.internal.helpers import safe_run_sql
sql_files = [
    {sql_files_str}
]
class Migration(migrations.Migration):
    dependencies = {dependencies}
    operations = safe_run_sql(sql_files)
"""
        with open(migration_file_path, 'w') as migration_file:
            migration_file.write(migration_content)
        self.stdout.write(
            self.style.SUCCESS(
                f"Migration file created at: {migration_file_path}\n"
                f"Dependencies set to: {dependencies}"
            )
        )
