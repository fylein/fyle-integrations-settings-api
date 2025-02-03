from apps.bamboohr.models import BambooHr
from apps.integrations.models import Integration
from apps.travelperk.models import TravelPerk

# Expected output:
# travelperk_created = 24
# bamboo_created = 44


travelperk_created = 0
for tp_object in TravelPerk.objects.all():
    _, created = Integration.objects.update_or_create(
        org_id=tp_object.org.id,
        type='TRAVEL',
        defaults={
            'is_active': True,
            'org_name': tp_object.org.name,
            'tpa_id': 'tpayrBcJzWAlx',
            'tpa_name': 'Fyle TravelPerk Integration',
            'connected_at': tp_object.created_at
        }
    )
    travelperk_created += created

print(f'{travelperk_created = }')

bamboo_created = 0
for bamboo_object in BambooHr.objects.all():
    _, created = Integration.objects.update_or_create(
        org_id=bamboo_object.org.id,
        type='TRAVEL',
        defaults={
            'is_active': True,
            'org_name': bamboo_object.org.name,
            'tpa_id': 'tpayrBcJzWAlx',
            'tpa_name': 'Fyle BambooHR Integration',
            'connected_at': bamboo_object.created_at
        }
    )
    bamboo_created += created

print(f'{bamboo_created = }')
