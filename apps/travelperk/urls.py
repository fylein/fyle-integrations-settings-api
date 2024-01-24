from django.urls import path

from .views import (
    TravelperkView, 
    ConnectTravelperkView,
    TravelperkWebhookAPIView, 
    DisconnectTravelperkView
)

app_name = 'travelperk'

urlpatterns = [
    path('', TravelperkView.as_view(), name='travelperk'),
    path('connect/', ConnectTravelperkView.as_view(), name='connect-travelperk'),
    path('disconnect/', DisconnectTravelperkView.as_view(), name='disconnect-travelperk'),
    path('travelperk_webhook/', TravelperkWebhookAPIView.as_view(), name='travelperk-webhook'),
]
