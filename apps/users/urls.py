from django.urls import path

from .views import  UserProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    #path('test/', TestView.as_view(), name='test')
]
