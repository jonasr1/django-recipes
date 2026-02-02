from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsOwner(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:  # noqa: ANN001
        return obj.author == request.user
