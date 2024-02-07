from django.urls import path, include

from .views import  OrgsView, ReadyView, WorkspaceAdminsView, SyncCategories

org_app_path = [
    path('', OrgsView.as_view(), name='orgs'),
    path('ready/', ReadyView.as_view(), name='ready'),
    path('<int:org_id>/admins/', WorkspaceAdminsView.as_view(), name='admin-view'),
    path('<int:org_id>/sync_categories/', SyncCategories.as_view(), name='sync-categories')
]

integration_paths = [
    path('<int:org_id>/bamboohr/', include('apps.bamboohr.urls', namespace = 'bamboohr')),
    path('<int:org_id>/travelperk/', include('apps.travelperk.urls', namespace = 'travelperk')),
]

urlpatterns = [*org_app_path, *integration_paths]
