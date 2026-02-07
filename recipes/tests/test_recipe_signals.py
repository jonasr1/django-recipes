import io
import os
import tempfile
from collections.abc import Sequence

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from recipes.models import Category, Recipe


def make_test_image(
    name: str = "test.jpg",
    size: tuple[int, int] = (10, 10),
    color: Sequence[int] = (255, 0, 0),
) -> SimpleUploadedFile:
    file = io.BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type="image/jpeg")


class RecipeCoverTest(TestCase):
    def test_create_recipe_with_cover(self) -> None:
        with (
            tempfile.TemporaryDirectory() as media_root,
            override_settings(MEDIA_ROOT=media_root),
        ):
            user = User.objects.create_user(username="u1", password="pass")  # noqa: S106
            category = Category.objects.create(name="Cat")
            cover = make_test_image()
            recipe = Recipe.objects.create(
                title="R1",
                description="desc",
                preparation_time=10,
                preparation_time_unit="Minutos",
                servings=2,
                servings_unit="Porções",
                preparation_steps="steps",
                author=user,
                category=category,
                cover=cover,
            )
            self.assertTrue(recipe.cover.name)

    def test_update_recipe_cover_deletes_old_file(self) -> None:
        with (
            tempfile.TemporaryDirectory() as media_root,
            override_settings(MEDIA_ROOT=media_root),
        ):
            user = User.objects.create_user(username="u1", password="pass")  # noqa: S106
            category = Category.objects.create(name="Cat")
            recipe = Recipe.objects.create(
                title="R1",
                description="desc",
                preparation_time=10,
                preparation_time_unit="Minutos",
                servings=2,
                servings_unit="Porções",
                preparation_steps="steps",
                author=user,
                category=category,
                cover=make_test_image("old.jpg"),
            )
            old_path = recipe.cover.path
            self.assertTrue(os.path.exists(old_path))
            recipe.cover = make_test_image("new.jpg")
            recipe.save()
            self.assertFalse(os.path.exists(old_path))
            self.assertTrue(os.path.exists(recipe.cover.path))

    def test_delete_recipe_cover_deletes_file(self) -> None:
        with (
            tempfile.TemporaryDirectory() as media_root,
            override_settings(MEDIA_ROOT=media_root),
        ):
            user = User.objects.create_user(username="u1", password="pass")  # noqa: S106
            category = Category.objects.create(name="Cat")
            recipe = Recipe.objects.create(
                title="R1",
                description="desc",
                preparation_time=10,
                preparation_time_unit="Minutos",
                servings=2,
                servings_unit="Porções",
                preparation_steps="steps",
                author=user,
                category=category,
                cover=make_test_image("duck.jpg"),
            )
            cover_path = recipe.cover.path
            self.assertTrue(os.path.exists(cover_path))
            recipe.delete()
            self.assertFalse(os.path.exists(cover_path))
