from django.urls import path, include

from .views import  OrgsView, ReadyView, CreateManagedUserInWorkato, FyleConnection, SendgridConnection, WorkspaceAdminsView

org_app_path = [
    path('', OrgsView.as_view(), name='orgs'),
    path('<int:org_id>/workato_workspace/', CreateManagedUserInWorkato.as_view(), name='workato-workspace'),
    path('ready/', ReadyView.as_view(), name='ready'),
    path('<int:org_id>/connect_fyle/', FyleConnection.as_view(), name='fyle-connection'),
    path('<int:org_id>/sendgrid_connection/', SendgridConnection.as_view(), name='sendgrid'),
    path('<int:org_id>/admins/', WorkspaceAdminsView.as_view(), name='admin-view')

]

integration_paths = [
    path('<int:org_id>/bamboohr/', include('apps.bamboohr.urls')),
    path('<int:org_id>/travelperk/', include('apps.travelperk.urls'))
]

urlpatterns = [*org_app_path, *integration_paths]
