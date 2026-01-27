from django.urls import path

from recipes.views import api

urlpatterns = [
    path("recipes/api/v2/", api.RecipeAPIv2List.as_view(), name="recipe-list-api"),
    path(
        "recipes/api/v2/<int:pk>/",
        api.RecipeAPIv2Detail.as_view(),
        name="api-detail-v2",
    ),
    path(
        "recipes/api/v2/tag/<int:pk>/",
        api.tag_api_detail,
        name="tag-api-detail",
    ),
]
