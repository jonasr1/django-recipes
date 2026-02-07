from unittest.mock import patch

from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from recipes.models import Recipe
from recipes.tests.api.mixins import RecipeAPIMixin
from tag.models import Tag


class RecipeAPIv2Test(APITestCase, RecipeAPIMixin):

    def test_recipe_api_list_returns_status_code_200(self) -> None:
        response = self.get_recipe_api_list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("recipes.views.api.RecipeAPIv2Pagination.page_size", new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self) -> None:
        wanted_number_of_recipes = 7
        self.create_recipes(9, recipe_kwargs={"is_published": True})
        response = self.get_recipe_api_list()
        qtd_of_loaded_recipes = len(response.data.get("results"))
        self.assertEqual(wanted_number_of_recipes, qtd_of_loaded_recipes)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 9)
        self.assertEqual(len(response.data["results"]), 7)
        self.assertIsNotNone(response.data["next"])

    def test_recipe_api_list_filters_by_category_id(self) -> None:
        category_1 = self.make_category(name="Category 1")
        category_2 = self.make_category(name="Category 2")
        recipe_1 = self.make_recipe(
            category=category_1,
            is_published=True,
            slug="r1",
            author={"username": "u1"},
        )
        recipe_2 = self.make_recipe(
            category=category_2,
            is_published=True,
            slug="r2",
            author={"username": "u2"},
        )
        url = self.build_url(
            "recipes:recipes-api-list",
            url_kwargs={},
            query_params={"category_id": category_1.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [recipe["id"] for recipe in response.data["results"]]
        self.assertIn(recipe_1.id, returned_ids)
        self.assertNotIn(recipe_2.id, returned_ids)

    def test_recipe_api_list_returns_only_published_recipes(self) -> None:
        published_recipe = self.make_recipe(is_published=True)
        unpublished_recipe = self.make_recipe(
            is_published=False,
            slug="r2",
            author={"username": "u2"},
        )
        response = self.get_recipe_api_list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [recipe["id"] for recipe in response.data["results"]]
        self.assertIn(published_recipe.id, returned_ids)
        self.assertNotIn(unpublished_recipe.id, returned_ids)

    def test_recipe_api_detail_returns_404_for_unpublished_recipe(self) -> None:
        recipe = self.make_recipe(is_published=False)
        api_url = reverse("recipes:recipes-api-detail", kwargs={"pk": recipe.pk})
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_recipe_api_create_requires_authentication(self) -> None:
        api_url = reverse("recipes:recipes-api-list")
        response = self.client.post(api_url, data={
            "title": "Recipe title",
            "description": "Recipe description",
            "preparation_time": 10,
            "preparation_time_unit": "Minutos",
            "servings": 4,
            "servings_unit": "Porções",
            "preparation_steps": "Recipe preparation steps",
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recipe_api_list_logged_user_can_create_a_recipe(self) -> None:
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data["jwt_access_token"]
        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f"Bearer {jwt_access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_recipe_api_create_uses_authenticated_user_as_author(self) -> None:
        user = self.make_author(username="author")
        self.client.force_authenticate(user=user)
        api_url = reverse("recipes:recipes-api-list")
        response = self.client.post(api_url, data={
            "title": "Recipe title",
            "description": "Recipe description",
            "preparation_time": 10,
            "preparation_time_unit": "Minutos",
            "servings": 4,
            "servings_unit": "Porções",
            "preparation_steps": "Recipe preparation steps",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], user.username)
        created_recipe = Recipe.objects.get(pk=response.data["id"])
        self.assertEqual(created_recipe.author, user)

    def test_recipe_api_partial_update_requires_owner(self) -> None:
        owner = self.make_author(username="owner")
        other_user = self.make_author(username="other")
        recipe = self.make_recipe(author=owner, is_published=True)
        self.client.force_authenticate(user=other_user)
        api_url = reverse("recipes:recipes-api-detail", kwargs={"pk": recipe.pk})
        response = self.client.patch(api_url, data={"title": "New recipe title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        recipe.refresh_from_db()
        self.assertNotEqual(recipe.title, "New recipe title")

    def test_recipe_api_partial_update_allows_owner(self) -> None:
        owner = self.make_author(username="owner")
        recipe = self.make_recipe(author=owner, is_published=True)
        self.client.force_authenticate(user=owner)
        api_url = reverse("recipes:recipes-api-detail", kwargs={"pk": recipe.pk})
        response = self.client.patch(api_url, data={"title": "New recipe title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, "New recipe title")

    def test_recipe_api_list_logged_user_can_update_a_recipe(self) -> None:
        # Arrange (config do test)
        recipe = self.make_recipe(is_published=True)
        access_data = self.get_auth_data(username="test_patch")
        jwt_access_token = access_data["jwt_access_token"]
        author = access_data["user"]
        recipe.author = author
        recipe.save()
        wanted_new_title = f"This new title updated by {author.username}"
        # Action
        response = self.client.patch(
            reverse("recipes:recipes-api-detail", args=(recipe.id,)),
            data={"title": wanted_new_title},
            HTTP_AUTHORIZATION=f"Bearer {jwt_access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), wanted_new_title)

    def test_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_another_user(self):  # noqa
        # Arrange (config do test)
        recipe = self.make_recipe(is_published=True)
        access_data = self.get_auth_data(username="test_patch")
        # This user cannot update the recipe because it is owned by another
        # user.
        another_user = self.get_auth_data(username="cant_update")
        jwt_access_token_from_another_user = another_user.get(
            "jwt_access_token",
        )
        # This is the actual owner of the recipe
        author = access_data.get("user")
        recipe.author = author
        recipe.save()
        # Action
        response = self.client.patch(
            reverse("recipes:recipes-api-detail", args=(recipe.id,)),
            data={},
            HTTP_AUTHORIZATION=f"Bearer {jwt_access_token_from_another_user}",
        )
        # Assertion
        # Another user cannot update the recipe, so the status code
        # must be 403 Forbidden
        self.assertEqual(
            response.status_code,
            403,
        )


class TagAPIDetailTest(APITestCase):
    def test_tag_api_detail_returns_tag_data(self) -> None:
        tag = Tag.objects.create(name="Italian")
        api_url = reverse("recipes:tag-api-detail", kwargs={"pk": tag.pk})
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], tag.id)
        self.assertEqual(response.data["name"], tag.name)
        self.assertEqual(response.data["slug"], tag.slug)

    def test_tag_api_detail_returns_404_when_tag_does_not_exist(self) -> None:
        api_url = reverse("recipes:tag-api-detail", kwargs={"pk": 9999})
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
