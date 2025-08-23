from typing import Any

from django import forms

from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Type your username")
        add_placeholder(self.fields["password"], "Type your password")

    username = forms.CharField(max_length=150, strip=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=128)
