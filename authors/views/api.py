from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authors.serializers import AuthorCreateSerializer, AuthorSerializer


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  # noqa: RUF012
    http_method_names = ["get", "post", "head", "options"]  # noqa: RUF012

    def get_permissions(self):  # noqa: ANN201
        if self.action == "create":
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):  # noqa: ANN201
        if self.action == "create":
            return AuthorCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self) -> QuerySet:
        User = get_user_model()  # noqa: N806
        if not self.request.user.is_authenticated:
            return User.objects.none()
        return User.objects.filter(username=self.request.user.username)

    @action(methods=["GET"], detail=False)
    def me(self, request) -> Response:  # noqa: ANN001
        obj = self.get_queryset().first()
        serializer = AuthorSerializer(instance=obj)
        return Response(data=serializer.data)
