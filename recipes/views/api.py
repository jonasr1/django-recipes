from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.views import get_object_or_404
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


class RecipeAPIv2List(APIView):
    def get(self, request: Request) -> Response:
        recipes = Recipe.objects.get_published()[0:10]
        serializer = RecipeSerializer(recipes, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RecipeAPIv2Detail(APIView):
    def get_recipe(self, pk: int) -> Response:
        return get_object_or_404(Recipe, is_published=True, pk=pk)

    def get(self, request: Request, pk: int) -> Response:
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(recipe, context={"request": request})
        return Response(serializer.data)

    def delete(self, request: Request, pk: int) -> Response:
        recipe = self.get_recipe(pk)
        recipe.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, pk: int) -> Response:
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            recipe, request.data, context={"request": request}, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(["GET"])  # type: ignore[misc]
def tag_api_detail(request: Request, pk: int) -> Response:
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(tag)
    return Response(serializer.data)
