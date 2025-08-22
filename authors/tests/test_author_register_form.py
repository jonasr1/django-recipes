from unittest import TestCase

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.constants import EMAIL_HELP_TEXT, PASSWORD_COMPLEXITY_ERROR
from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ("username", "Your username"),
        ("first_name", "Ex.: John"),
        ("email", "Your e-mail"),
        ("last_name", "Ex.: Doe"),
        ("password", "Type your password"),
        ("password2", "Repeat your password"),
    ])
    def test_fields_placeholder(self, field: str, placeholder: str) -> None:
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(
            current_placeholder,
            placeholder,
            f"Placeholder for field '{field}' is wrong.",
        )

    def test_field_email_help_text(self) -> None:
        form = RegisterForm()
        current = form["email"].field.help_text
        self.assertEqual(
            current,
            EMAIL_HELP_TEXT,
            f"Email help_text mismatch. Got: '{current}'",
        )


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@anyemail.com",
            "password": "Str0ngP@ssword1",
            "password2": "Str0ngP@ssword1",
        }
        return super().setUp()

    @property
    def url(self) -> str:
        return reverse("authors:create")

    def post_data(self) -> HttpResponse:
        return self.client.post(self.url, data=self.form_data, follow=True)

    @parameterized.expand([
        ("username", "This field must not be empty"),
        ("first_name", "Write your first name"),
        ("last_name", "Write your last name"),
        ("email", "E-mail is required"),
        ("password", "Password must not be empty"),
        ("password2", "Please, repeat your password"),
    ])
    def test_fields_cannot_be_empty(self, field: str, msg: str) -> None:
        self.form_data[field] = ""
        response = self.post_data()
        self.assertIn(msg, response.context["form"].errors.get(field))
        self.assertIn(msg, response.content.decode("utf-8"))

    def test_username_field_min_length_should_be_4(self) -> None:
        self.form_data["username"] = "joa"
        response = self.post_data()
        username_len = len(self.form_data["username"])
        msg = f"Ensure this value has at least 4 characters (it has {username_len})."
        self.assertIn(msg, response.context["form"].errors.get("username"))
        self.assertIn(msg, response.content.decode("utf-8"))

    def test_username_field_max_length_should_be_150(self) -> None:
        self.form_data["username"] = "A" * 151
        response = self.post_data()
        username_len = len(self.form_data["username"])
        msg = f"Ensure this value has at most 150 characters (it has {username_len})."
        self.assertIn(msg, response.context["form"].errors.get("username"))
        self.assertIn(msg, response.content.decode("utf-8"))

    def test_password_accepts_strong_passwords(self) -> None:
        self.form_data["password"] = "Abc_123!"  # noqa: S105
        response = self.post_data()
        self.assertNotIn(
            PASSWORD_COMPLEXITY_ERROR, response.context["form"].errors.get("password")
        )
        self.assertNotIn(PASSWORD_COMPLEXITY_ERROR, response.content.decode("utf-8"))

    def test_password_rejects_weak_passwords(self) -> None:
        self.form_data["password"] = "abc123"  # noqa: S105
        response = self.post_data()
        self.assertIn(
            PASSWORD_COMPLEXITY_ERROR, response.context["form"].errors.get("password")
        )
        self.assertIn(PASSWORD_COMPLEXITY_ERROR, response.content.decode("utf-8"))

    def test_send_get_request_to_registration_create_view_returns_404(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_register_create_with_valid_form_creates_user_and_clears_session(
        self,
    ) -> None:
        response = self.post_data()
        self.assertTrue(User.objects.filter(username="user").exists())
        # Check if the session was cleared
        self.assertNotIn("register_form_data", self.client.session)
        # Check if the success message exists
        messages = list(response.context["messages"])
        self.assertTrue(any("Your user is created" in str(m) for m in messages))

    def test_register_create_with_invalid_form_keeps_session_data(self) -> None:
        self.form_data["username"] = ""
        self.form_data["password"] = ""
        response = self.client.post(self.url, self.form_data)
        self.assertFalse(User.objects.exists())
        # Keeps data in the session
        self.assertIn("register_form_data", self.client.session)
        # Redirects correctly
        self.assertRedirects(response, reverse("authors:register"))

    def test_email_field_must_be_unique_when_submitting_form(self) -> None:
        # First submission to create the user
        self.post_data()
        # Second submission with same email should trigger validation error
        response = self.post_data()
        msg = "User e-mail is already in use"
        self.assertIn(msg, response.context["form"].errors.get("email"))
        self.assertIn(msg, response.content.decode("utf-8"))

    def test_author_created_can_login(self) -> None:
        password = "B#c342435"  # noqa: S105
        self.form_data.update(
            {"username": "testuser", "password": password, "password2": password})
        self.client.post(self.url, data=self.form_data)
        is_authenticated = self.client.login(username="testuser", password=password)
        self.assertTrue(is_authenticated, "The newly created user should be able to log in")  # noqa: E501
