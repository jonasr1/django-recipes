# ruff: noqa: RUF012
import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

EMAIL_HELP_TEXT = "The e-mail must be valid"


def add_attr(field: forms.Field, attr_name: str, new_attr_val: str) -> None:
    existing_attrs = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing_attrs} {new_attr_val}".strip()


def add_placeholder(field: forms.Field, placeholder_val: str) -> None:
    add_attr(field, "placeholder", placeholder_val)


def strong_password(password: str) -> None:
    regex = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")
    if not regex.match(password):
        password_regex_error = (
            "Password must have at least one uppercase letter, "  # noqa: S105
            "one lowercase letter and one number. The length should be"
            "at least 8 characters."
        )
        raise ValidationError(
            (password_regex_error),
            code="invalid",
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Your username")
        add_placeholder(self.fields["email"], "Your e-mail")
        add_placeholder(self.fields["first_name"], "Ex.: John")
        add_placeholder(self.fields["last_name"], "Ex.: Doe")
        add_placeholder(self.fields["password"], "Type your password")
        add_placeholder(self.fields["password2"], "Repeat your password")

    first_name = forms.CharField(
        error_messages={"required": "Write your first name"},
    )
    last_name = forms.CharField(
        error_messages={"required": "Write your last name"},
    )
    email = forms.EmailField(
        error_messages={"required": "E-mail is required"},
        help_text=EMAIL_HELP_TEXT
    )
    password = forms.CharField(
        error_messages={"required": "Password must not be empty"},
        widget=forms.PasswordInput(),
        validators=[strong_password],
    )
    password2 = forms.CharField(
        error_messages={"required": "Please, repeat your password"},
        widget=forms.PasswordInput(),
        validators=[strong_password],
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password")
        error_messages = {"username": {"required": "This field must not be empty."}}

    def clean(self) -> None:
        cleaned_data = super().clean()
        password = cleaned_data.get("password") if cleaned_data else None
        password2 = cleaned_data.get("password2") if cleaned_data else None
        if password != password2:
            password_confirmation_error = ValidationError(
                "Password and password2 must be equal", code="invalid"
            )
            raise ValidationError({
                "password": password_confirmation_error,
                "password2": [
                    password_confirmation_error,
                ],
            })
