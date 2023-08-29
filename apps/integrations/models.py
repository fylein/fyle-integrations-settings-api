from django.db import models

INTEGRATION_TYPE = (('ACCOUNTING', 'ACCOUNTING'), ('HRMS', 'HRMS'), ('TRAVEL', 'TRAVEL'), ('PAYROLL', 'PAYROLL'))


class Integration(models.Model):
    id = models.AutoField(primary_key=True, help_text='Unique Id to indentify an Integration')
    tpa_id = models.CharField(max_length=255, help_text='Third Party App Id')
    tpa_name = models.CharField(max_length=255, help_text='Third Party App Name')
    org_id = models.CharField(max_length=255, help_text='Org Id')
    type = models.CharField(max_length=255, help_text='Type of Integration', choices=INTEGRATION_TYPE)
    is_active = models.BooleanField(default=False, help_text='Is Integration Active')
    is_beta = models.BooleanField(default=False, help_text='Is Beta')
    connected_at = models.DateTimeField(auto_now_add=True, help_text='Connected at datetime')
    disconnected_at = models.DateTimeField(null=True, help_text='Disconnected at datetime')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at datetime')

    class Meta:
        db_table = 'integrations'
        unique_together = ('tpa_id', 'org_id', 'type')
