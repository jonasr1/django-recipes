from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from authors.views import get_object_or_404
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


@api_view(["GET", "POST"])  # type: ignore[misc]  # noqa: RET503
def recipe_api_list(request: HttpRequest) -> Response:  # pyright: ignore[reportReturnType]
    if request.method == "GET":
        recipes = Recipe.objects.get_published()[0:10]
        serializer = RecipeSerializer(recipes, many=True, context={"request": request})
        return Response(serializer.data)
    if request.method == "POST":
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(["GET", "DELETE", "PATCH"])  # type: ignore[misc]
def recipe_api_detail(request: HttpRequest, pk: int) -> Response:
    recipe = get_object_or_404(Recipe, is_published=True, pk=pk)
    if request.method == "GET":
        serializer = RecipeSerializer(recipe, context={"request": request})
        return Response(serializer.data)
    if request.method == "PATCH":
        serializer = RecipeSerializer(
            recipe, request.data, context={"request": request}, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == "DELETE":
        recipe.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    return None


@api_view(["GET"])  # type: ignore[misc]
def tag_api_detail(request: Request, pk: int) -> Response:
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(tag)
    return Response(serializer.data)
