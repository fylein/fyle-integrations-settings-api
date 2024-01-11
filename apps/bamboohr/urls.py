from django.urls import path

from .views import BambooHrConnection, BambooHrView, BambooHrConfigurationView, \
    DisconnectView, SyncEmployeesView, HealthCheck, WebhookCallbackAPIView

app_name = 'bamboohr'

urlpatterns = [
    path('webhook_callback/', WebhookCallbackAPIView.as_view(), name='webhook-callback'),
    path('health_check/', HealthCheck.as_view(), name='health-check'),
    path('', BambooHrView.as_view(), name='bamboohr'),
    path('bamboo_connection/', BambooHrConnection.as_view(), name='connection'),
    path('configuration/', BambooHrConfigurationView.as_view(), name='configuration'),
    path('refresh_employees/', SyncEmployeesView.as_view(), name='sync-employees'),
    path('disconnect/', DisconnectView.as_view(), name='disconnect'),
]
