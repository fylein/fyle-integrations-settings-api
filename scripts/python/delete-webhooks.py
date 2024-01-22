from apps.bamboohr.models import BambooHr
from bamboosdk.bamboohrsdk import BambooHrSDK

org_ids = [164, 922]

for org_id in org_ids:
    try:
        bamboohr = BambooHr.objects.get(org_id = org_id)
        bambamboohrsdk = BambooHrSDK(api_token=bamboohr.api_token, sub_domain=bamboohr.sub_domain)
        response = bambamboohrsdk.webhook.delete(id=bamboohr.webhook_id)
        print('For org_id {bamboohr.org.id}', response)
    except Exception as e:
        print(f'For org_id {bamboohr.org.id} error occured', e)
