from django.urls import path

from .views import TravelperkView, PostPackage, PostFolder, TravelperkConnection, \
    TravekPerkConfigurationView, AwsS3Connection, GenerateToken

urlpatterns = [
    path('', TravelperkView.as_view(), name='travelperk'),
    path('packages/', PostPackage.as_view(), name='travelperk-package'),
    path('folder/', PostFolder.as_view(), name='travelperk-folder'),
    path('configurations/', TravekPerkConfigurationView.as_view(), name='travelperk-configuration'),
    path('travelperk_connection/', TravelperkConnection.as_view(), name='fyle-travelperk-connection'),
    path('s3_connection/', AwsS3Connection.as_view(), name='s3-connection'),
    path('generate_token/', GenerateToken.as_view(), name='generate-token'),
]
