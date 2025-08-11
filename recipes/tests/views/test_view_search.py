from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self) -> None:
        url = reverse("recipes:search")
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)  # type: ignore

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

    def test_recipe_search_can_find_recipe_by_title(self) -> None:
        title1 = "This is recipe one"
        title2 = "This is recipe two"

        recipe1 = self.make_recipe(slug="one", title=title1,author={"username": "one"})
        recipe2 = self.make_recipe(slug="two", title=title2,author={"username": "two"})

        search_url = reverse("recipes:search")
        response1 = self.client.get(f"{search_url}?q={title1}")
        response2 = self.client.get(f"{search_url}?q={title2}")
        response_both = self.client.get(f"{search_url}?q=this")

        self.assertIn(member=recipe1, container=response1.context["recipes"])
        self.assertNotIn(member=recipe2, container=response1.context["recipes"])

        self.assertIn(member=recipe2, container=response2.context["recipes"])
        self.assertNotIn(member=recipe1, container=response2.context["recipes"])

        self.assertIn(member=recipe1, container=response_both.context["recipes"])
        self.assertIn(member=recipe2, container=response_both.context["recipes"])

    def test_recipe_search_is_paginated(self) -> None:
        term = "bolo"
        self.assertPaginationWorks(
            "recipes:search",
            query_params={"q": term},
            recipe_kwargs={"title": f"{term} incrível"},
        )
