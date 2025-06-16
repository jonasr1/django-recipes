from django.test import TestCase

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

    def make_recipe(
        self,
        category: dict[str, str] | None = None,
        author: dict[str, str] | None = None,
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
        if category is None:
            category = {}
        if author is None:
            author = {}
        return Recipe.objects.create(
                description=description, author=self.make_author(**author),
                preparation_time=preparation_time,
                preparation_time_unit=preparation_time_unit,
                servings=servings, servings_unit=servings_unit, title=title,
                preparation_steps=preparation_steps, is_published=is_published,
                preparation_steps_is_html=preparation_steps_is_html, slug=slug,
                category=self.make_category(**category)
        )
