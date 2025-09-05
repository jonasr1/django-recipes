from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorsLogoutTest(TestCase):
    def setUp(self) -> None:
        self.username = "test_user"
        self.password = "test_pass"  # noqa: S105
        self.user = User.objects.create_user(
            username=self.username, password=self.password,
        )

    def test_logout_via_get_returns_invalid_request_message(self) -> None:
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("authors:logout"), follow=True)
        self.assertIn("Invalid logout request", response.content.decode())

    def test_user_can_logout_successfully(self) -> None:
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(
            reverse("authors:logout"), follow=True, data={"username": "my_user"},
        )
        self.assertIn("Logged out successfully", response.content.decode())
