from django.urls import path

from .views import IntegrationsView

app_name = 'integrations'

urlpatterns = [
    path('', IntegrationsView.as_view(), name='integrations'),
]
