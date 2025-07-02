from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self) -> None:
        url = reverse("recipes:search")
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self) -> None:
        url = reverse("recipes:search")
        response = self.client.get(url + "?q=teste")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self) -> None:
        url = reverse("recipes:search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_title_and_escaped(self) -> None:
        url = reverse("recipes:search")
        response = self.client.get(url + "?q=<Teste>")
        self.assertIn("Search for &#x27;&lt;Teste&gt;", response.content.decode("utf-8"))  # noqa: E501
