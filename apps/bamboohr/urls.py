from django.urls import path

from .views import RecipeView

urlpatterns = [
    path('recipes/', RecipeView.as_view(), name='recipes')
]
