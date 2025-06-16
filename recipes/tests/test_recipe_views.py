from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
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

    def test_recipe_category_template_loads_recipes(self) -> None:
        needed_title = "This is category test"
        #  Need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse("recipes:category", args=(1,)))
        content = response.content.decode("utf-8")
        self.assertIn(needed_title, content)

    def test_recipe_category_view_returnss_404_if_no_recipes_found(self) -> None:
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_dont_load_recipes_not_published(self) -> None:
        """Test recipe is_published False dont show"""
        #  Need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse(
                "recipes:category", kwargs={"category_id": recipe.category.id}) # type: ignore
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_function_is_correct(self) -> None:
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self) -> None:
        view = resolve(reverse("recipes:recipe", args=(1,)))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returnss_404_if_no_recipes_found(self) -> None:
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"pk": 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self) -> None:
        needed_title = "This is a detail page - It load one recipe"
        #  need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse("recipes:recipe", kwargs={"pk": 1}))
        content = response.content.decode("utf-8")
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self) -> None:
        """Test recipe is_published False dont show"""
        #  Need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"pk": recipe.id})
        )
        self.assertEqual(response.status_code, 404)
