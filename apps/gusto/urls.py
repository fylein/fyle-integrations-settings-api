from django.urls import path

from .views import PostFolder, PostPackage, DisconnectView, GustoConfigurationView, SyncEmployeesView, GustoConnection

urlpatterns = [
    path('packages/', PostPackage.as_view(), name='package'),
    path('folder/', PostFolder.as_view(), name='folder'),
    path('gusto_connection/', GustoConnection.as_view(), name='gusto-connection'),
    path('configuration/', GustoConfigurationView.as_view(), name='configuration'),
    path('refresh_employees/', SyncEmployeesView.as_view(), name='sync-employees'),
    path('disconnect/', DisconnectView.as_view(), name='disconnect'),
]
