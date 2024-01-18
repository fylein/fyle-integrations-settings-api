
from django.db.models.signals import post_save
from django.dispatch import receiver
from admin_settings.settings import API_URL

from bamboosdk.bamboohrsdk import BambooHrSDK
from apps.bamboohr.models import BambooHr

@receiver(post_save, sender=BambooHr)
def run_post_save_bamboohr_triggers(sender, instance: BambooHr, **kwargs):

    bamboohrsdk = BambooHrSDK(api_token=instance.api_token, sub_domain=instance.sub_domain)

    webhook_payload = {
        'postFields': {
            'firstName': 'firstName',
            'lastName': 'lastName',
            'department': 'department',
            'workEmail': 'workEmail',
            'status': 'status',
            'supervisorEId': 'supervisorEId'
        },
        'name': instance.org.name,
        'monitorFields': ['firstName', 'lastName', 'department', 'workEmail', 'status', 'reportingTo'],
        'url': API_URL + f'/orgs/{instance.org.id}/bamboohr/webhook_callback/',
        'format': 'json'
    }

    response = bamboohrsdk.webhook.post(payload=webhook_payload)
    private_key = response['privateKey']
    BambooHr.objects.filter(id=instance.id).update(webhook_id=int(response['id']), private_key=private_key)
