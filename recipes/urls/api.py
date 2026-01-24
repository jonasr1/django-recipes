from django.urls import path

from recipes.views import api

urlpatterns = [
    path("recipes/api/v2/", api.recipe_api_list, name="recipe-list-api"),
    path(
        "recipes/api/v2/<int:pk>/",
        api.recipe_api_detail,
        name="api-detail-v2",
    ),
    path(
        "recipes/api/v2/tag/<int:pk>/",
        api.tag_api_detail,
        name="tag-api-detail",
    ),
]
