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
    path("recipes/tags/<slug:slug>", views.RecipeListViewTag.as_view(), name="tag"),
    path("recipes/api/v1/", views.RecipeListViewHomeApi.as_view(), name="api-list"),
    path(
        "recipes/api/v1/<int:pk>/",
        views.RecipeDetailApi.as_view(),
        name="api-detail",
    ),
    path(
        "recipes/api/v1/category/<int:category_id>/",
        views.RecipeListViewCategoryApi.as_view(),
        name="category-api",
    ),
    path(
        "recipes/search/api/v1/",
        views.RecipeListViewSearchApi.as_view(),
        name="search-api",
    ),
    path("recipes/theory/", views.theory, name="theory"),
]
