from django.urls import path

from apps.travelperk.views import (
    TravelperkView, 
    ConnectTravelperkView,
    TravelperkWebhookAPIView, 
    DisconnectTravelperkView,
    TravelperkPaymentProfileMappingView,
    SyncPaymentProfiles,
    AdvancedSettingView
)

app_name = 'travelperk'

urlpatterns = [
    path('', TravelperkView.as_view(), name='travelperk'),
    path('connect/', ConnectTravelperkView.as_view(), name='connect-travelperk'),
    path('disconnect/', DisconnectTravelperkView.as_view(), name='disconnect-travelperk'),
    path('travelperk_webhook/', TravelperkWebhookAPIView.as_view(), name='travelperk-webhook'),
    path('advanced_settings/', AdvancedSettingView.as_view(), name='advance-settings-view'),
    path('profile_mappings/', TravelperkPaymentProfileMappingView.as_view(), name='profile-mappings'),
    path('sync_payment_profile/', SyncPaymentProfiles.as_view(), name='sync-payment-profiles'),
]
