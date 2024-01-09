
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
            'status': 'status'
        },
        'name': instance.org.name,
        'monitorFields': ['firstName', 'lastName', 'department', 'workEmail', 'status'],
        'url': 'https://localhost:8006/' + f'api/orgs/{instance.org.id}/bamboohr/webhook_callback/',
        'format': 'json'
    }

    response = bamboohrsdk.webhook.post(payload=webhook_payload)
    BambooHr.objects.filter(id=instance.id).update(webhook_id=int(response['id']))
