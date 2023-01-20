
from django.db.models.signals import pre_save
from django.dispatch import receiver

from workato import Workato
from apps.bamboohr.models import BambooHrConfiguration
from apps.orgs.models import Org

@receiver(pre_save, sender=BambooHrConfiguration)
def run_pre_save_configuration_triggers(sender, instance: BambooHrConfiguration, **kwargs):
    connector = Workato()
    org = Org.objects.get(id=instance.org_id)
    connector.recipes.post(org.managed_user_id, instance.recipe_id, None, 'stop')
