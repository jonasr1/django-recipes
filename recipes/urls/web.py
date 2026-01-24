from django.urls import path

from recipes.views import site

urlpatterns = [
    path("", site.RecipeListViewHome.as_view(), name="home"),
    path("recipes/search/", site.RecipeListViewSearch.as_view(), name="search"),
    path(
        "recipes/category/<int:category_id>/",
        site.RecipeListViewCategory.as_view(),
        name="category",
    ),
    path("recipes/<int:pk>/", site.RecipeDetail.as_view(), name="recipe"),
    path("recipes/tags/<slug:slug>", site.RecipeListViewTag.as_view(), name="tag"),
    path("recipes/api/v1/", site.RecipeListViewHomeApi.as_view(), name="api-list"),
    path(
        "recipes/api/v1/<int:pk>/",
        site.RecipeDetailApi.as_view(),
        name="api-detail",
    ),
    path(
        "recipes/api/v1/category/<int:category_id>/",
        site.RecipeListViewCategoryApi.as_view(),
        name="category-api",
    ),
    path(
        "recipes/search/api/v1/",
        site.RecipeListViewSearchApi.as_view(),
        name="search-api",
    ),
    path("recipes/theory/", site.theory, name="theory"),
]
