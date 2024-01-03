
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from admin_settings.settings import API_URL

from workato import Workato

from bamboosdk.bamboohrsdk import BambooHrSDK
from apps.bamboohr.models import BambooHrConfiguration, BambooHr
from apps.orgs.models import Org

@receiver(pre_save, sender=BambooHrConfiguration)
def run_pre_save_configuration_triggers(sender, instance: BambooHrConfiguration, **kwargs):
    connector = Workato()
    org = Org.objects.get(id=instance.org_id)
    connector.recipes.post(org.managed_user_id, instance.recipe_id, None, 'stop')


@receiver(post_save, sender=BambooHr)
def run_post_save_bamboohr_triggers(sender, instance: BambooHr, **kwargs):

    # Disconnect the signal to avoid triggering it again
    post_save.disconnect(run_post_save_bamboohr_triggers, sender=BambooHr)

    bamboohrsdk = BambooHrSDK(api_token=instance.api_token, sub_domain=instance.sub_domain)
    
    webhook_payload = {
        'postFields': {
            'firstName': 'firstName',
            'lastName': 'lastName',
            'department': 'department',
            'workEmail': 'workEmail',
            'status': 'status'
        },
        'name': instance.org.name,
        'monitorFields': ['firstName', 'lastName', 'department', 'workEmail', 'reportingTo', 'status'],
        'url': API_URL + f'/orgs/{instance.org.id}/bamboohr/webhook_callback/',
        'format': 'json'
    }

    response = bamboohrsdk.webhook.post(payload=webhook_payload)
    instance.webhook_id = int(response['id'])
    instance.save()

    # Reconnect the signal after saving
    post_save.connect(run_post_save_bamboohr_triggers, sender=BambooHr)
