from django.test import TestCase
from django.urls import reverse


class RecipeURLTest(TestCase):
    def test_recipe_home_url_is_correct(self) -> None:
        url = reverse("recipes:home")
        self.assertEqual(url, "/")

    def test_recipe_category_url_is_correct(self) -> None:
        url = reverse("recipes:category", kwargs={"category_id": 1})
        self.assertEqual(url, "/recipes/category/1/")

    def test_recipe_detail_url_is_correct(self) -> None:
        url = reverse("recipes:recipe", args=(1,))
        self.assertEqual(url, "/recipes/1/")
