from collections import defaultdict

from django.forms import ValidationError

from utils.validators import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data: dict, errors: dict | None = None, error_class: type | None = None) -> None:  # noqa: E501
        self.errors = defaultdict(list) if (errors is None) else errors
        self.error_class = ValidationError if (error_class is None) else error_class
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):  # noqa
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()
        title = self.data.get("title")
        description = self.data.get("description")
        if title == description:
            self.errors["title"].append("Cannot be equal to description.")
            self.errors["description"].append("Cannot be equal to title.")
        if self.errors:
            raise self.error_class(self.errors)

    def clean_title(self) -> str | None:
        title = self.data.get("title")
        if not title or len(title) < 5:
            self.errors["title"].append("Must have at least 5 characters.")
        return title

    def clean_preparation_time(self) -> int | None:
        return self._validate_positive("preparation_time")

    def clean_servings(self) -> int | None:
        return self._validate_positive("servings")

    def _validate_positive(self, field_name: str) -> int | None:
        value = self.data.get(field_name)
        if value is None or not is_positive_number(value):
            self.errors[field_name].append("Must be a positive number.")
            return None
        return value
