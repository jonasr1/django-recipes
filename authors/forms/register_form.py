
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from authors.constants import (
    COMMON_LENGTH_ERRORS,
    EMAIL_HELP_TEXT,
    PLACEHOLDERS,
)
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        for field, placeholder in PLACEHOLDERS.items():
            add_placeholder(self.fields[field], placeholder)

    username = forms.CharField(
        help_text=(
            "Username must have letters, numbers or one of those @.+-_. "
            "The length should be between 4 and 150 characters."
        ),
        error_messages={
            "required": "This field must not be empty",
            **COMMON_LENGTH_ERRORS,
        },
        min_length=4,
        max_length=150,
    )
    first_name = forms.CharField(
        error_messages={"required": "Write your first name"},
    )
    last_name = forms.CharField(
        error_messages={"required": "Write your last name"},
    )
    email = forms.EmailField(
        error_messages={"required": "E-mail is required"},
        help_text=EMAIL_HELP_TEXT,
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

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email", "")
        exists = User.objects.filter(email=email).exists()
        if exists:
            msg = "User e-mail is already in use"
            raise ValidationError(msg)
        return email

    def clean(self) -> None:
        cleaned_data = super().clean()
        password = cleaned_data.get("password") if cleaned_data else None
        password2 = cleaned_data.get("password2") if cleaned_data else None
        if password != password2:
            password_confirmation_error = ValidationError(
                "Password and password2 must be equal", code="invalid",
            )
            raise ValidationError({
                "password": password_confirmation_error,
                "password2": [
                    password_confirmation_error,
                ],
            })
