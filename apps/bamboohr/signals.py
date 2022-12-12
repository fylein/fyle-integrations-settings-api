
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from workato import Workato
import json

from apps.bamboohr.models import Configuration
from apps.orgs.models import Org

@receiver(pre_save, sender=Configuration)
def run_pre_save_configuration_triggers(sender, instance: Configuration, **kwargs):
    connector = Workato()
    if instance.recipe_status:
        org = Org.objects.get(id=instance.org_id)
        print('nilesh')
        connector.recipes.post(org.managed_user_id, instance.recipe_id, None, 'stop')
