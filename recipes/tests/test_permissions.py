from django.test import TestCase
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.test import APIRequestFactory

from recipes.permissions import IsOwner
from recipes.tests.test_recipe_base import RecipeMixin
from recipes.views.api import RecipeAPIv2ViewSet


class IsOwnerPermissionTest(TestCase, RecipeMixin):
    def setUp(self) -> None:
        super().setUp()
        self.factory = APIRequestFactory()
        self.permission = IsOwner()

    def test_has_object_permission_returns_true_for_owner(self) -> None:
        recipe = self.make_recipe()
        request = self.factory.get("/")
        request.user = recipe.author
        self.assertTrue(self.permission.has_object_permission(request, None, recipe))

    def test_has_object_permission_returns_false_for_non_owner(self) -> None:
        recipe = self.make_recipe()
        request = self.factory.get("/")
        request.user = self.make_author(username="other-user")
        self.assertFalse(self.permission.has_object_permission(request, None, recipe))


class RecipeAPIv2PermissionsTest(TestCase):
    def test_get_permissions_partial_update_returns_auth_and_owner(self) -> None:
        view = RecipeAPIv2ViewSet()
        view.action = "partial_update"
        perms = view.get_permissions()

        self.assertEqual(
            {type(p) for p in perms},
            {IsAuthenticatedOrReadOnly, IsOwner},
        )

    def test_get_permissions_destroy_returns_auth_and_owner(self) -> None:
        view = RecipeAPIv2ViewSet()
        view.action = "destroy"
        perms = view.get_permissions()

        self.assertEqual(
            {type(p) for p in perms},
            {IsAuthenticatedOrReadOnly, IsOwner},
        )

    def test_get_permissions_default_returns_only_auth_readonly(self) -> None:
        view = RecipeAPIv2ViewSet()
        view.action = "list"
        perms = view.get_permissions()

        self.assertEqual(
            [type(p) for p in perms],
            [IsAuthenticatedOrReadOnly],
        )
