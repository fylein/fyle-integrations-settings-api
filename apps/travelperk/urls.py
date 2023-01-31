from django.urls import path

from .views import TravelperkView, PostPackage, PostFolder, FyleTravelperkConnection, \
    TravekPerkConfigurationView, AwsS3Connection

urlpatterns = [
    path('', TravelperkView.as_view(), name='travelperk'),
    path('packages/', PostPackage.as_view(), name='travelperk-package'),
    path('folder/', PostFolder.as_view(), name='travelperk-folder'),
    path('configurations/', TravekPerkConfigurationView.as_view(), name='travelperk-configuration'),
    path('fyle_connection/', FyleTravelperkConnection.as_view(), name='fyle-travelperk-connection'),
    path('s3_connection/', AwsS3Connection.as_view(), name='s3-connection')
]
