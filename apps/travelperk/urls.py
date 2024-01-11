from django.urls import path

from .views import TravelperkView, PostPackage, PostFolder, TravelperkConnection, \
    TravekPerkConfigurationView, AwsS3Connection, RecipeStatusView, ConnectTravelperkView, \
    TravelperkWebhookAPIView, DisconnectTravelperkView, TravelperkPaymentProfileMappingView

app_name = 'travelperk'

urlpatterns = [
    path('', TravelperkView.as_view(), name='travelperk'),
    path('packages/', PostPackage.as_view(), name='package'),
    path('folder/', PostFolder.as_view(), name='folder'),
    path('configurations/', TravekPerkConfigurationView.as_view(), name='configuration'),
    path('recipe_status/', RecipeStatusView.as_view(), name='recipe-status'),
    path('travelperk_connection/', TravelperkConnection.as_view(), name='fyle-connection'),
    path('s3_connection/', AwsS3Connection.as_view(), name='s3-connection'),
    path('connect/', ConnectTravelperkView.as_view(), name='connect-travelperk'),
    path('disconnect/', DisconnectTravelperkView.as_view(), name='disconnect-travelperk'),
    path('travelperk_webhook/', TravelperkWebhookAPIView.as_view(), name='travelperk-webhook'),
    path('profile_mappings/', TravelperkPaymentProfileMappingView.as_view(), name='profile-mappings')
]
