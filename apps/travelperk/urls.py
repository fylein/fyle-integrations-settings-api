from django.urls import path

from .views import TravelperkView, PostPackage, PostFolder, TravelperkConnection, \
    TravekPerkConfigurationView, AwsS3Connection, RecipeStatusView, ConnectTravelperkView

urlpatterns = [
    path('', TravelperkView.as_view(), name='travelperk'),
    path('packages/', PostPackage.as_view(), name='travelperk-package'),
    path('folder/', PostFolder.as_view(), name='travelperk-folder'),
    path('configurations/', TravekPerkConfigurationView.as_view(), name='travelperk-configuration'),
    path('recipe_status/', RecipeStatusView.as_view(), name='recipe-status-view'),
    path('travelperk_connection/', TravelperkConnection.as_view(), name='fyle-travelperk-connection'),
    path('s3_connection/', AwsS3Connection.as_view(), name='s3-connection'),
    path('connect/', ConnectTravelperkView.as_view(), name='connect-travelperk'),
]
