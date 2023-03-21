from django.urls import path

from .views import PostFolder, PostPackage, GustoConfigurationView, SyncEmployeesView, GustoView, GustoConnection, RecipeStatusView

urlpatterns = [
    path('', GustoView.as_view(), name="gusto"),
    path('packages/', PostPackage.as_view(), name='gusto_package'),
    path('folder/', PostFolder.as_view(), name='gusto_folder'),
    path('configuration/', GustoConfigurationView.as_view(), name='gusto_configuration'),
    path('refresh_employees/', SyncEmployeesView.as_view(), name='gusto_sync_employees'),
    path('gusto_connection/', GustoConnection.as_view(), name='gusto_fyle_connection'),
    path('recipe_status/', RecipeStatusView.as_view(), name='gusto_recipe_status')
]
