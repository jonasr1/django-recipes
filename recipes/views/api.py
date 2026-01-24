from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from authors.views import get_object_or_404
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


@api_view(["GET"])  # type: ignore[misc]
def recipe_api_list(request: Request) -> Response:
    recipes = Recipe.objects.get_published()[0:10]
    serializer = RecipeSerializer(recipes, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])  # type: ignore[misc]
def recipe_api_detail(request: Request, pk: int) -> Response:
    recipe = get_object_or_404(Recipe, is_published=True, pk=pk)
    serializer = RecipeSerializer(recipe, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])  # type: ignore[misc]
def tag_api_detail(request: Request, pk: int) -> Response:
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(tag)
    return Response(serializer.data)
