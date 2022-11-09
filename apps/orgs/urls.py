from django.urls import path

from .views import ReadyView

urlpatterns = [
     path('ready/', ReadyView.as_view(), name='ready')
]
