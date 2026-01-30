from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from recipes.views import RecipeAPIv2ViewSet, api

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register("recipes/api/v2", RecipeAPIv2ViewSet, "recipes-api")


urlpatterns = [
    path(
        "recipes/api/v2/tag/<int:pk>/",
        api.tag_api_detail,
        name="tag-api-detail",
    ),
    path("recipes/api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "recipes/api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh",
    ),
    path("recipes/api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(recipe_api_v2_router.urls)),
]
