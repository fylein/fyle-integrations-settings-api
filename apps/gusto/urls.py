from django.urls import path

from .views import PostFolder, PostPackage, GustoConfigurationView, SyncEmployeesView, GustoView, GustoConnection, RecipeStatusView

app_name = 'gusto'

urlpatterns = [
    path('', GustoView.as_view(), name="gusto"),
    path('packages/', PostPackage.as_view(), name='package'),
    path('folder/', PostFolder.as_view(), name='folder'),
    path('configuration/', GustoConfigurationView.as_view(), name='configuration'),
    path('refresh_employees/', SyncEmployeesView.as_view(), name='sync_employees'),
    path('connection/', GustoConnection.as_view(), name='fyle_connection'),
    path('recipe_status/', RecipeStatusView.as_view(), name='recipe_status')
]
