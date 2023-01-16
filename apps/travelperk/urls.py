from django.urls import path

from .views import TravelperkView, PostPackage, PostFolder, FyleTravelperkConnection, TravekPerkConfigurationView

urlpatterns = [
    path('', TravelperkView.as_view(), name='travelperk'),
    path('packages/', PostPackage.as_view(), name='package'),
    path('folder/', PostFolder.as_view(), name='folder'),
    path('configurations/', TravekPerkConfigurationView.as_view(), name='travelperk-configuration'),
    path('fyle_connection/', FyleTravelperkConnection.as_view(), name='fyle-travelperk-connection')
]
