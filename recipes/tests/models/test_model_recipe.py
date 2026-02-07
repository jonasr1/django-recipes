import tempfile
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import override_settings
from parameterized import parameterized
from PIL import Image as PilImage

from recipes.models import Recipe
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self) -> Recipe:
        recipe = Recipe(
            category=self.make_category(name="Test Defaults"),
            author=self.make_author(username="newuser"),
            title="Recipe title",
            description="Recipe description",
            slug="recipe-slug-for-no-defaults",
            preparation_time=10,
            preparation_time_unit="Minutos",
            servings=5,
            servings_unit="Porções",
            preparation_steps="Recipe Preparation Steps",
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([  # type: ignore
        ("title", 65),
        ("description", 165),
        ("servings_unit", 65),
        ("preparation_time_unit", 65),
    ])
    def test_recipe_fields_max_length(self, field: str, max_length: int) -> None:
        setattr(self.recipe, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self) -> None:
        recipe = self.make_recipe(
            slug="html-is-false-by-default",
            author=self.make_author(username="html_is_false"),
        )
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg="Recipe preparation_steps_is_html is not False",
        )

    def test_recipe_is_published_is_false_by_default(self) -> None:
        recipe = self.make_recipe(
            slug="published-is-false-by-default",
            title="Is Published is false by default",
            author=self.make_author(username="published is false"),
        )
        self.assertFalse(
            recipe.is_published,
            msg="Recipe is_published is not False",
        )

    def test_recipe_string_representation(self) -> None:
        needed = "Testing Representation"
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), needed,
            msg=f"Recipe string representation must be '{needed}' but"
                f"'{self.recipe!s}' was received",
        )

    def test_recipe_save_generates_unique_slug(self) -> None:
        author = self.make_author(username="slugger")
        recipe_1 = self.make_recipe(title="Slug Test Recipe", slug="", author=author)
        recipe_2 = self.make_recipe(title="Slug Test Recipe", slug="", author=author)
        self.assertEqual(recipe_1.slug, "slug-test-recipe")
        self.assertEqual(recipe_2.slug, "slug-test-recipe-1")

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_resize_image_reduces_width(self) -> None:
        media_root = Path(settings.MEDIA_ROOT)
        image_path = media_root / "test-image.jpg"
        PilImage.new("RGB", (1200, 800)).save(image_path)

        class DummyImage:
            name = "test-image.jpg"
        recipe = Recipe()
        recipe.resize_image(DummyImage(), new_width=840)
        with PilImage.open(image_path) as img:
            self.assertEqual(img.size[0], 840)
            self.assertEqual(img.size[1], round((800 * 840) / 1200))

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_resize_image_skips_if_smaller(self) -> None:
        media_root = Path(settings.MEDIA_ROOT)
        image_path = media_root / "small.jpg"
        PilImage.new("RGB", (800, 600)).save(image_path)

        class DummyImage:
            name = "small.jpg"
        recipe = Recipe()
        recipe.resize_image(DummyImage(), new_width=840)
        with PilImage.open(image_path) as img:
            self.assertEqual(img.size, (800, 600))
