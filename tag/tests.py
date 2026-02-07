from unittest.mock import patch

from django.test import TestCase
from django.utils.text import slugify

from tag.models import Tag


class TagModelTest(TestCase):
    def test_the_test(self) -> None:
        tag = Tag.objects.create(name="test_tag")
        self.assertEqual(str(tag), tag.name)

    def test_slug_is_generated_when_missing(self) -> None:
        with patch("tag.models.SystemRandom.choices", return_value=list("abc12")):
            tag = Tag.objects.create(name="test_tag")

        self.assertEqual(tag.slug, slugify("test_tag-abc12"))

    def test_slug_is_preserved_when_provided(self) -> None:
        tag = Tag.objects.create(name="test_tag", slug="my-custom-slug")
        self.assertEqual(tag.slug, "my-custom-slug")
