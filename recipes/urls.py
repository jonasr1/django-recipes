from django.urls import path

from recipes import views

app_name = "recipes" # pylint: disable=invalid-name


urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/category/<int:category_id>/", views.category, name="category"),
    path("recipes/<int:pk>/", views.recipe, name="recipe"),
]
