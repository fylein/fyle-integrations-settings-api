from apps.travelperk.models import TravelperkCredential
from apps.travelperk.serializers import SyncPaymentProfileSerializer


all_creds = TravelperkCredential.objects.all()

for creds in all_creds:
    SyncPaymentProfileSerializer().sync_payment_profiles(creds.org_id)
