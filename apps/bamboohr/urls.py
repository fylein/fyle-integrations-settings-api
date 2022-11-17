from django.urls import path

<<<<<<< HEAD
from .views import  FyleConnection, ReadyView, RecipeView

urlpatterns = [
    path('connect_fyle/', FyleConnection.as_view({'post': 'post'}), name='fyle-connection'),
    path('recipes/', RecipeView.as_view({'get': 'get'}, name='recipes')),
    path('recipes/<int:recipe_id>/', RecipeView.as_view({'get': 'get_by_id'}), name='recipe-by-id')
=======
from .views import RecipeView

urlpatterns = [
    path('recipes/', RecipeView.as_view(), name='recipes')
>>>>>>> 0082f3715dc041c8c98a6af68c737e20ac632dc1
]
