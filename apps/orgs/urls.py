from django.urls import path, include

from .views import  ManagedUser, OrgsView, ReadyView

org_app_path = [
    path('', OrgsView.as_view({'get': 'get', 'post': 'post'}), name='orgs'),
    path('<int:org_id>/', OrgsView.as_view({'get': 'get_by_id'}), name='org-by-id'),
    path('<int:org_id>/connect_workato', OrgsView.as_view({'post': 'post'}), name='connect workato'),
    path('<int:org_id>/managed_users/', ManagedUser.as_view({'get': 'get', 'post': 'post'}), name='managed-users'),
    path('ready/', ReadyView.as_view({'get': 'get'}), name='ready'),
]

other_app_path = [
    path('<int:org_id>/bamboohr/', include('apps.bamboohr.urls'))
]

urlpatterns = []
urlpatterns.extend(org_app_path)
urlpatterns.extend(other_app_path)
