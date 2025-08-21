from typing import Any
from unittest.mock import patch

from django.http.response import HttpResponse
from django.test import TestCase
from django.urls.base import reverse

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):

    def make_category(self, name: str = "category") -> Category:
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name: str = "user",
        last_name: str = "name",
        username: str = "username",
        password: str = "1234567",  # noqa: S107
        email: str = "username@gmail.com",
    ) -> User:
        return User.objects.create_user(
            first_name=first_name, last_name=last_name, username=username,
            password=password, email=email
        )

    def make_many_recipes(self, amount: int = 8) -> None:
        for i in range(amount):
            self.make_recipe(slug=f"r{i}", author={"username": f"u{i}"})

    def make_recipe(
        self,
        category: Category | dict[str, str] | None = None,
        author: User | dict[str, str] | None = None,
        title: str = "Recipe title",
        description: str = "Recipe description",
        slug: str = "recipe-slug",
        preparation_time: int = 10,
        preparation_time_unit: str = "Minutos",
        servings: int = 5,
        servings_unit: str = "Porções",
        preparation_steps: str = "Recipe Preparation Steps",
        *, preparation_steps_is_html: bool = False,
        is_published: bool = True,
    ) -> Recipe:
        cat_instance = (
            category
            if isinstance(category, Category)
            else self.make_category(**(category or {}))
        )
        author_instance = (
            author if isinstance(author, User) else self.make_author(**(author or {}))
        )
        return Recipe.objects.create(
            description=description, author=author_instance,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings, servings_unit=servings_unit, title=title,
            preparation_steps=preparation_steps, is_published=is_published,
            preparation_steps_is_html=preparation_steps_is_html, slug=slug,
            category=cat_instance
        )

    def create_recipes(self, total_items: int, recipe_kwargs: dict[str, Any]) -> None:
        for i in range(total_items):
            kwargs = {"slug": f"r{i}", "author": {"username": f"u{i}"}}
            kwargs.update(recipe_kwargs)
            self.make_recipe(**kwargs)

    def build_url(
        self, url_name: str, url_kwargs: dict[str, Any], query_params: dict[str, Any]
    ) -> str:
        url = reverse(url_name, kwargs=url_kwargs)
        if query_params:
            from urllib.parse import urlencode
            url = f"{url}?{urlencode(query_params)}"
        return url

    def check_pagination(
        self, response: HttpResponse, total_items: int, per_page: int
    ) -> None:
        self.assertIn("recipes", response.context)
        recipes = response.context["recipes"]
        paginator = recipes.paginator
        expected_pages = (total_items + per_page - 1) // per_page
        self.assertEqual(paginator.num_pages, expected_pages)
        for page_num in range(1, expected_pages + 1):
            page = paginator.get_page(page_num)
            expected_len = (
                per_page
                if page_num < expected_pages
                # Last page may have fewer items
                else total_items - per_page * (expected_pages - 1)
            )
            self.assertEqual(len(page), expected_len)
        all_ids: set[int] = set()
        for page_num in paginator.page_range:
            ids = {r.id for r in paginator.get_page(page_num)}
            self.assertTrue(all_ids.isdisjoint(ids))
            all_ids.update(ids)

    def assertPaginationWorks(  # noqa: N802
        self,
        url_name: str,
        total_items: int = 8,
        per_page: int = 3,
        url_kwargs: dict[str, Any] | None = None,
        recipe_kwargs: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
    ) -> None:
        url_kwargs = url_kwargs or {}
        recipe_kwargs = recipe_kwargs or {}
        query_params = query_params or {}
        self.create_recipes(total_items, recipe_kwargs=recipe_kwargs)
        with patch("recipes.views.PER_PAGE", new=per_page):
            url = self.build_url(url_name, url_kwargs, query_params)
            response = self.client.get(url)
            self.check_pagination(response, total_items, per_page)
