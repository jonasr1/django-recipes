from django.urls import path

from recipes import views

app_name = "recipes"


urlpatterns = [
    path("", views.RecipeListViewHome.as_view(), name="home"),
    path("recipes/search/", views.RecipeListViewSearch.as_view(), name="search"),
    path(
        "recipes/category/<int:category_id>/",
        views.RecipeListViewCategory.as_view(),
        name="category",
    ),
    path("recipes/<int:pk>/", views.RecipeDetail.as_view(), name="recipe"),
    path("recipes/api/v1/", views.RecipeListViewHomeApi.as_view(), name="recipes_api"),
    path(
        "recipes/api/v1/<int:pk>/",
        views.RecipeDetailApi.as_view(),
        name="recipe_api_detail",
    ),
    path(
        "recipes/api/v1/category/<int:category_id>/",
        views.RecipeListViewCategoryApi.as_view(),
        name="category_api",
    ),
    path(
        "recipes/search/api/v1/",
        views.RecipeListViewSearchApi.as_view(),
        name="search_api",
    ),
]
