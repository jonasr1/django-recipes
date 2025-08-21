
from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    @property
    def url(self) -> str:
        return reverse("recipes:home")

    def test_recipe_home_view_function_is_correct(self) -> None:
        view = resolve(self.url)
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_200_status(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self) -> None:
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self) -> None:
        response = self.client.get(self.url)
        self.assertIn(
            "No recipes found here 🥲", response.content.decode("utf-8")
        )

    def test_recipe_home_template_loads_recipes(self) -> None:
        #  need a recipe for this test
        self.make_recipe()
        response = self.client.get(self.url)
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]
        self.assertIn("Recipe title", content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self) -> None:
        """Test recipe is_published False dont show"""
        #  Need a recipe for this test
        self.make_recipe(is_published=False)
        response = self.client.get(self.url)
        self.assertIn(
            "No recipes found here 🥲", response.content.decode("utf-8")
        )

    def test_recipe_home_is_paginated(self) -> None:
        self.assertPaginationWorks("recipes:home", total_items=8, per_page=3)

    def test_invalid_page_query_falls_back_to_page_one(self) -> None:
        self.make_many_recipes()  # creates 8 recipes by default
        with patch("recipes.views.PER_PAGE", new=3):
            response = self.client.get(self.url + "?page=12A")
            self.assertEqual(response.context["recipes"].number, 1)

    def test_valid_page_queries_work_normally(self) -> None:
        self.make_many_recipes()  # creates 8 recipes by default
        with patch("recipes.views.PER_PAGE", new=3):
            response = self.client.get(self.url + "?page=2")
            self.assertEqual(response.context["recipes"].number, 2)
            response = self.client.get(self.url + "?page=3")
            self.assertEqual(response.context["recipes"].number, 3)
