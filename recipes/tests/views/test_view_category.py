from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_template_loads_recipes(self) -> None:
        needed_title = "This is category test"
        #  Need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse("recipes:category", args=(1,)))
        content = response.content.decode("utf-8")
        self.assertIn(needed_title, content)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self) -> None:
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000}),
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_dont_load_recipes_not_published(self) -> None:
        """Test recipe is_published False dont show"""
        #  Need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse(
            "recipes:category", kwargs={"category_id": recipe.category.id}),  # type: ignore  # noqa: E501, RUF100
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_function_is_correct(self) -> None:
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_is_paginated(self) -> None:
        category = self.make_category(name="Sobremesas")
        self.assertPaginationWorks(
            "recipes:category",
            url_kwargs={"category_id": category.pk},
            recipe_kwargs={"category": category},
        )
