from django.urls import path, include

from .views import  OrgsView, ReadyView, CreateWorkatoWorkspace, FyleConnection 

org_app_path = [
    path('', OrgsView.as_view(), name='orgs'),
    path('ready/', ReadyView.as_view(), name='ready'),
    path('<int:org_id>/workato_workspace/', CreateWorkatoWorkspace.as_view()),
    path('<int:managed_user_id>/connect_fyle/', FyleConnection.as_view(), name='fyle-connection'),
]

integration_paths = [
    path('<int:org_id>/bamboohr/', include('apps.bamboohr.urls'))
]

urlpatterns = [*org_app_path, *integration_paths]
