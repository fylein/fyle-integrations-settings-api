from django.urls import path

from .views import PostFolder, PostPackage, BambooHrConnection, BambooHrView

urlpatterns = [
    path('', BambooHrView.as_view(), name='bamboohr'),
    path('packages/', PostPackage.as_view(), name='package'),
    path('folder/', PostFolder.as_view(), name='folder'),
    path('bamboo_connection/', BambooHrConnection.as_view(), name='bamboo-connection'),
]
