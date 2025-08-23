import re

from django import forms
from django.core.exceptions import ValidationError

from authors.constants import PASSWORD_COMPLEXITY_ERROR


def add_attr(field: forms.Field, attr_name: str, new_attr_val: str) -> None:
    existing_attrs = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing_attrs} {new_attr_val}".strip()


def add_placeholder(field: forms.Field, placeholder_val: str) -> None:
    add_attr(field, "placeholder", placeholder_val)


def strong_password(password: str) -> None:
    regex = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")
    if not regex.match(password):
        password_regex_error = PASSWORD_COMPLEXITY_ERROR
        raise ValidationError(
            (password_regex_error),
            code="invalid",
        )
