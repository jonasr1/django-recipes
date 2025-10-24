from django import forms

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.validators import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        add_attr(self.fields["preparation_steps"], "class", "span-2")

    class Meta:
        model = Recipe
        fields = (
            "title",
            "description",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
        )
        widgets = {  # noqa: RUF012
            "cover": forms.FileInput(attrs={"class": "span-2"}),
        }

    def clean(self, *args, **kwargs):  # noqa
        cleaned_data = super().clean(*args, **kwargs)
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")
        if title == description:
            self.add_error("title", "Cannot be equal to description.")
            self.add_error("description", "Cannot be equal to title.")
        return cleaned_data

    def clean_title(self) -> str | None:
        title = self.cleaned_data.get("title")
        if not title or len(title) < 5:
            self.add_error("title", "Must have at least 5 characters.")
        return title

    def clean_preparation_time(self) -> int | None:
        return self._validate_positive("preparation_time")

    def clean_servings(self) -> int | None:
        return self._validate_positive("servings")

    def _validate_positive(self, field_name: str) -> int | None:
        value = self.cleaned_data.get(field_name)
        if value is None or not is_positive_number(value):
            self.add_error(field_name, "Must be a positive number.")
            return None
        return value
