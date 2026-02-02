from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from authors.serializers import AuthorSerializer


class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  # noqa: RUF012

    def get_queryset(self) -> QuerySet:
        User = get_user_model()  # noqa: N806
        return User.objects.filter(username=self.request.user.username)

    @action(methods=["GET"], detail=False)
    def me(self, request) -> Response:  # noqa: ANN001
        obj = self.get_queryset().first()
        serializer = AuthorSerializer(instance=obj)
        return Response(data=serializer.data)
