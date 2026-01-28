from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from authors.views import get_object_or_404
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 8


class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination


class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

    def patch(self, request: Request, *args, **kwargs) -> Response:
        pk = kwargs.get("pk")

        recipe = self.get_queryset().filter(pk=pk).first()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )


@api_view(["GET"])  # type: ignore[misc]
def tag_api_detail(request: Request, pk: int) -> Response:
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(tag)
    return Response(serializer.data)
