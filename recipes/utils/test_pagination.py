from unittest import TestCase

from recipes.utils.pagination import make_pagination


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self) -> None:
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )["pagination"]
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self) -> None:  # noqa: E501
        # Current page = 1 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )["pagination"]
        self.assertEqual([1, 2, 3, 4], pagination)
        # Current page = 2 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2
        )["pagination"]
        self.assertEqual([1, 2, 3, 4], pagination)
        # Current page = 3 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3
        )["pagination"]
        self.assertEqual([2, 3, 4, 5], pagination)
        # Current page = 4 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4
        )["pagination"]
        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_sure_middle_ranges_are_correct(self) -> None:
        # Current page = 3 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=13
        )["pagination"]
        self.assertEqual([12, 13, 14, 15], pagination)
        # Current page = 4 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=14
        )["pagination"]
        self.assertEqual([13, 14, 15, 16], pagination)

    def test_make_pagination_range_is_static_when_last_range_page_is_next(self) -> None:
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)
        pagination = make_pagination(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)
