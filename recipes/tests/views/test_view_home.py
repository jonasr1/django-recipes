from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self) -> None:
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_200_status(self) -> None:
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self) -> None:
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self) -> None:
        response = self.client.get(reverse("recipes:home"))
        self.assertIn(
            "No recipes found here 🥲", response.content.decode("utf-8")
        )

    def test_recipe_home_template_loads_recipes(self) -> None:
        #  need a recipe for this test
        self.make_recipe()
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")
        response_context_recipes = response.context["recipes"]
        self.assertIn("Recipe title", content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self) -> None:
        """Test recipe is_published False dont show"""
        #  Need a recipe for this test
        self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:home"))
        self.assertIn(
            "No recipes found here 🥲", response.content.decode("utf-8")
        )

    def test_recipe_home_is_paginated(self) -> None:
        for i in range(8):
            kwargs = {"slug": f"r{i}", "author": {"username": f"u{i}"} }
            self.make_recipe(**kwargs)
        with patch("recipes.views.PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:home"))
            self.assertIn("recipes", response.context)
            recipes = response.context["recipes"]
            paginator = recipes.paginator
            self.assertEqual(paginator.num_pages, 3)  # Check number of pages
            # Check items per page
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
            all_ids: set[int] = set()  # Check that there is no overlap between pages
            for page in paginator.page_range:
                ids = {r.id for r in paginator.get_page(page)}
                self.assertTrue(all_ids.isdisjoint(ids))
                all_ids.update(ids)
