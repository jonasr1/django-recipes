from typing import ClassVar
from unittest import TestCase

from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
from django.urls.base import reverse

from recipes.models import Category, Recipe
from recipes.utils.pagination import make_pagination_range


class PaginationLogicTest(TestCase):
    """Tests for the pagination logic without database interaction."""
    def test_pagination_static_for_early_pages(self) -> None:
        test_cases = [
            (1, [1, 2, 3, 4]), # Static range for page 1
            (2, [1, 2, 3, 4]), # Still static
            (3, [2, 3, 4, 5]), # Dynamic starts here
            (4, [3, 4, 5 ,6]), # Confirm dynamic continues
        ]
        for current_page, expected in test_cases:
            with self.subTest(current_page=current_page):
                result = self.get_pagination(current_page)
                self.assertEqual(result, expected)

    def test_pagination_dynamic_range_middle_pages(self) -> None:
        test_cases = [
            (13, [12, 13, 14, 15]),  # Dynamic range for page 13
            (14, [13, 14, 15, 16]),  # Dynamic range for page 14
        ]
        for current_page, expected in test_cases:
            with self.subTest(current_page=current_page):
                result = self.get_pagination(current_page)
                self.assertEqual(result, expected)

    def test_pagination_range_is_static_range_end(self) -> None:
        test_cases = [
            (18, [17, 18, 19, 20]),  # Static range
            (19, [17, 18, 19, 20]),  # Static range
            (20, [17, 18, 19, 20]),  # Static range
        ]
        for current_page, expected in test_cases:
            with self.subTest(current_page=current_page):
                result = self.get_pagination(current_page)
                self.assertEqual(result, expected)

    def test_invalid_current_page(self) -> None:
        for current_page in [0, 30]:
            with self.subTest(current_page=current_page), self.assertRaises(ValueError):
                make_pagination_range(
                    list(range(1, 21)), range_size=4, current_page=current_page
                )

    def get_pagination(self, current_page: int, range_size: int = 4) -> list[int]:
        return make_pagination_range(list(range(1, 21)), range_size, current_page)[
            "pagination"
        ]

class PaginationIntegrationTest(DjangoTestCase):
    """Tests for pagination integration with Recipe model."""
    user: ClassVar[User]
    category: ClassVar[Category]
    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data by creating a user, category, and 20 recipes."""
        cls.user = User.objects.create_user(username="testuser", password="testpass")  # noqa: S106
        cls.category = Category.objects.create(name="Test Category")
        for i in range(20):
            Recipe.objects.create(
                title=f"Recipe {i+1}",
                description="Test description",
                slug=f"recipe-{i+1}",
                preparation_time=30,
                preparation_time_unit="minutes",
                servings=4,
                servings_unit="people",
                preparation_steps="Test steps",
                author=cls.user,
                category=cls.category,
                is_published=True,
            )

    def test_fisrt_page_has_correct_number_of_itens(self)-> None:
        url = reverse("recipes:home")
        response = self.client.get(url)
        self.assertEqual(len(response.context["recipes"]), 9)
