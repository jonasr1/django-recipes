from django import forms

from recipes.models import Recipe
from utils.django_forms import add_attr


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
