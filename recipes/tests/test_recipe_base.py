from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name='category'):
        return Category.objects.create(name=name)

    def make_author(
        self, first_name='user', last_name='name', username='username',
        password='1234567', email='username@gmail.com'
    ):
        return User.objects.create_user(
            first_name=first_name, last_name=last_name, username=username,
            password=password, email=email
        )

    def make_recipe(
        self, category=None, author=None, title='Recipe title',
        description='Recipe description', slug='recipe-slug',
        preparation_time=10, preparation_time_unit='Minutos',
        servings=5, servings_unit='Porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False, is_published=True
    ):
        if category is None:
            category = {}
        if author is None:
            author = {}
        return Recipe.objects.create(  # noqa: F841
                description=description, author=self.make_author(**author),
                preparation_time=preparation_time,
                preparation_time_unit=preparation_time_unit,
                servings=servings, servings_unit=servings_unit, title=title,
                preparation_steps=preparation_steps, is_published=is_published,
                preparation_steps_is_html=preparation_steps_is_html, slug=slug,
                category=self.make_category(**category)
        )
