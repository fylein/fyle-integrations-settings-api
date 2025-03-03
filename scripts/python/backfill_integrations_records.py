from django.conf import settings
from apps.bamboohr.models import BambooHr
from apps.integrations.models import Integration
from apps.travelperk.models import TravelPerk

'''
Expected outputs:

US Cluster:
travelperk_created = 26
bamboo_created = 14

Indian Cluster:
travelperk_created = 1
bamboo_created = 1
'''

def main():
    travelperk_created = 0
    for tp_object in TravelPerk.objects.all():
        _, created = Integration.objects.update_or_create(
            org_id=tp_object.org.fyle_org_id,
            type='TRAVEL',
            defaults={
                'is_active': True,
                'org_name': tp_object.org.name,
                'tpa_id': settings.FYLE_CLIENT_ID,
                'tpa_name': 'Fyle TravelPerk Integration',
                'connected_at': tp_object.created_at
            }
        )
        travelperk_created += created
    print(f'{travelperk_created = }')
    bamboo_created = 0
    for bamboo_object in BambooHr.objects.filter(api_token__isnull=False, sub_domain__isnull=False):
        _, created = Integration.objects.update_or_create(
            org_id=bamboo_object.org.fyle_org_id,
            type='HRMS',
            defaults={
                'is_active': True,
                'org_name': bamboo_object.org.name,
                'tpa_id': settings.FYLE_CLIENT_ID,
                'tpa_name': 'Fyle BambooHR Integration',
                'connected_at': bamboo_object.created_at
            }
        )
        bamboo_created += created
    print(f'{bamboo_created = }')


main()

'''
Verify counts:

\c integration_settings
select count(*) from travelperk;
select count(*) from bamboohr where api_token is not null and sub_domain is not null;

select count(*) from integrations where type='TRAVEL';
select count(*) from integrations where type='HRMS';
'''