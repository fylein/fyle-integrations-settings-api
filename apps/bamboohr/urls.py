from django.urls import path

from .views import PostFolder, PostPackage, BambooHrConnection, BambooHrView, ConfigurationView, \
    DisconnectView, SyncEmployeesView

urlpatterns = [
    path('', BambooHrView.as_view(), name='bamboohr'),
    path('packages/', PostPackage.as_view(), name='package'),
    path('folder/', PostFolder.as_view(), name='folder'),
    path('bamboo_connection/', BambooHrConnection.as_view(), name='bamboo-connection'),
    path('configuration/', ConfigurationView.as_view(), name='configuration'),
    path('refresh_employees/', SyncEmployeesView.as_view(), name='sync-employees'),
    path('disconnect/', DisconnectView.as_view(), name='disconnect'),
]
