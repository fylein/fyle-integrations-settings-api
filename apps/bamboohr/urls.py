from django.urls import path

from .views import  FyleConnection, ReadyView, RecipeView

urlpatterns = [
    path('ready/', ReadyView.as_view({'get': 'get'}), name='new'),
    path('connect_fyle/', FyleConnection.as_view({'post': 'post'}), name='fyle-connection'),
    path('recipes/', RecipeView.as_view({'get': 'get'}, name='recipes')),
    path('recipes/<int:recipe_id>/', RecipeView.as_view({'get': 'get_by_id'}), name='recipe-by-id')
]
