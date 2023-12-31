from django.urls import path

from .views import PostFolder, PostPackage, BambooHrConnection, BambooHrView, BambooHrConfigurationView, \
    DisconnectView, SyncEmployeesView, HealthCheck

app_name = 'bamboohr'

urlpatterns = [
    path('health_check/', HealthCheck.as_view(), name='health-check'),
    path('', BambooHrView.as_view(), name='bamboohr'),
    path('packages/', PostPackage.as_view(), name='package'),
    path('folder/', PostFolder.as_view(), name='folder'),
    path('bamboo_connection/', BambooHrConnection.as_view(), name='connection'),
    path('configuration/', BambooHrConfigurationView.as_view(), name='configuration'),
    path('refresh_employees/', SyncEmployeesView.as_view(), name='sync-employees'),
    path('disconnect/', DisconnectView.as_view(), name='disconnect'),
]
