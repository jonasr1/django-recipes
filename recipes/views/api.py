# ruff: noqa: RUF012
from rest_framework import status
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
    http_method_names = ["GET", "PATCH", "DELETE", "HEAD", "OPTIONS"]

    def get_object(self) -> Recipe:
        pk: int = self.kwargs.get("pk", "")
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):  # noqa: ANN201
        if self.request.method in {"PATCH", "DELETE"}:
            return [IsAuthenticatedOrReadOnly(), IsOwner()]
        return super().get_permissions()

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers,
        )

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        recipe = self.get_object()
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
