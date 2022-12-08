
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from workato import Workato
import json

from apps.bamboohr.models import Configuration
from apps.orgs.models import Org

@receiver(post_save, sender=Configuration)
def run_post_configuration_triggers(sender, instance: Configuration, **kwargs):
    connector = Workato()
    org = Org.objects.get(id=instance.org_id)
    if instance.recipe_status:
        connector.recipes.post(org.managed_user_id, instance.recipe_id, None, 'stop')
