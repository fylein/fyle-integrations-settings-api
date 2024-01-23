from django.urls import path, include

from .views import  OrgsView, ReadyView, CreateManagedUserInWorkato, FyleConnection, SendgridConnection, \
    WorkspaceAdminsView, GenerateToken, SyncCategories

org_app_path = [
    path('', OrgsView.as_view(), name='orgs'),
    path('<int:org_id>/workato_workspace/', CreateManagedUserInWorkato.as_view(), name='workato-workspace'),
    path('ready/', ReadyView.as_view(), name='ready'),
    path('<int:org_id>/connect_fyle/', FyleConnection.as_view(), name='fyle-connection'),
    path('<int:org_id>/sendgrid_connection/', SendgridConnection.as_view(), name='sendgrid'),
    path('<int:org_id>/admins/', WorkspaceAdminsView.as_view(), name='admin-view'),
    path('<int:org_id>/generate_token/', GenerateToken.as_view(), name='generate-token'),
    path('<int:org_id>/sync_categories/', SyncCategories.as_view(), name='sync-categories')
]

integration_paths = [
    path('<int:org_id>/bamboohr/', include('apps.bamboohr.urls', namespace = 'bamboohr')),
    path('<int:org_id>/travelperk/', include('apps.travelperk.urls', namespace = 'travelperk')),
    path('<int:org_id>/gusto/', include('apps.gusto.urls', namespace = 'gusto'))
]

urlpatterns = [*org_app_path, *integration_paths]
