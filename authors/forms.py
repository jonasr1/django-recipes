# ruff: noqa: RUF012
from django import forms
from django.contrib.auth.models import User


def add_attr(field: forms.Field, attr_name: str, new_attr_val: str)-> None:
    existing_attrs = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing_attrs} {new_attr_val}".strip()

def add_placeholder(field: forms.Field, placeholder_val: str) -> None:
    add_attr(field, "placeholder", placeholder_val)

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Your username")
        add_placeholder(self.fields["email"], "Your e-mail")
        add_placeholder(self.fields["first_name"], "Ex: John")
        add_placeholder(self.fields["last_name"], "Ex: Doe")

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Type your password"}),
        help_text=(
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be"
            "at least 8 characters."
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat your password"}),
        help_text=(
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be"
            "at least 8 characters."
        ),
    )
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password")
        help_texts = {"email": "The e-mail must be valid"}
        error_messages = {
            "username": {"required": "This field must not be empty."}
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Type yourname here",
                    "class": "input text-input other-class",
                }
            ),
            "password": forms.PasswordInput(
                attrs={"placeholder": "Type your password here"}
            ),
        }
