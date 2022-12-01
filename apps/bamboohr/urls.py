from django.urls import path

from .views import RecipeView, PostFolder, PostPackage, BambooHrConnection, BambooHr

urlpatterns = [
    path('', BambooHr.as_view(), name='bamboohr'),
    path('recipes/', RecipeView.as_view(), name='recipes'),
    path('packages/', PostPackage.as_view(), name='package'),
    path('folder/', PostFolder.as_view(), name='folder'),
    path('bamboo_connection/', BambooHrConnection.as_view(), name='bamboo-connection'),
]

