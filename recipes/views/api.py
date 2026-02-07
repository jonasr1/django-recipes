# ruff: noqa: RUF012
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authors.views import get_object_or_404
from recipes.models import Recipe
from recipes.permissions import IsOwner
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 8


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_permissions(self):  # noqa: ANN201
        if self.action in {"partial_update", "destroy"}:
            return [IsAuthenticatedOrReadOnly(), IsOwner()]
        return super().get_permissions()

    def get_queryset(self):  # noqa: ANN201
        qs = super().get_queryset()
        category_id = self.request.query_params.get("category_id")
        if category_id and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)
        return qs

    def perform_create(self, serializer: RecipeSerializer) -> None:
        serializer.save(author=self.request.user)


@api_view(["GET"])  # type: ignore[misc]
def tag_api_detail(request: Request, pk: int) -> Response:
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(tag)
    return Response(serializer.data)
