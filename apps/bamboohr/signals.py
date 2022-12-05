
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from workato import Workato
import json

from apps.bamboohr.models import Configuration
from apps.orgs.models import Org

@receiver(pre_save, sender=Configuration)
def run_pre_configuration_triggers(sender, instance: Configuration, **kwargs):
    connector = Workato()
    org = Org.objects.get(id=instance.org_id)
    if instance.recipe_status:
        connector.recipes.post(org.managed_user_id, instance.recipe_id, 'stop')
    
@receiver(post_save, sender=Configuration)
def run_post_configration_triggers(sender, instance: Configuration, **kwargs):
    """
    :param sender: Sender Class
    :param instance: Row Instance of Sender Class
    :return: None
    """

    connector = Workato()
    org = Org.objects.get(id=instance.org_id)

    if instance.recipe_status:
        connector.recipes.post(org.managed_user_id, instance.recipe_id, 'start')