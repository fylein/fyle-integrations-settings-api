from apps.bamboohr.models import BambooHr
from bamboosdk.bamboohrsdk import BambooHrSDK
from admin_settings.settings import API_URL

all_bamboohr = BambooHr.objects.all()

for bamboohr in all_bamboohr:

    bamboohrsdk = BambooHrSDK(api_token=bamboohr.api_token, sub_domain=bamboohr.sub_domain)

    webhook_payload = {
        'postFields': {
            'firstName': 'firstName',
            'lastName': 'lastName',
            'department': 'department',
            'workEmail': 'workEmail',
            'status': 'status',
            'reportingTo': 'reportingTo'
        },
        'name': bamboohr.org.name,
        'monitorFields': ['firstName', 'lastName', 'department', 'workEmail', 'status', 'reportingTo'],
        'url': API_URL + f'/orgs/{bamboohr.org.id}/bamboohr/webhook_callback/',
        'format': 'json'
    }

    response = bamboohrsdk.webhook.post(payload=webhook_payload)
    BambooHr.objects.filter(id=bamboohr.id).update(webhook_id=int(response['id']))
