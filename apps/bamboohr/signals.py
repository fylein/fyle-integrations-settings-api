from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.bamboohr.models import BambooHrConfiguration
from apps.bamboohr.tasks import schedule_sync_employees


@receiver(post_save, sender=BambooHrConfiguration)
def run_post_save_configurations(sender, instance: BambooHrConfiguration, *args, **kwargs):
    schedule_sync_employees(org_id=instance.org.id)
