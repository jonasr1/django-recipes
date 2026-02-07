# ruff:noqa: S106
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthorAPITest(APITestCase):
    def test_author_me_returns_logged_user(self) -> None:
        User = get_user_model()  # noqa: N806
        user = User.objects.create_user(username="u1", password="pass")
        User.objects.create_user(username="u2", password="pass")

        self.client.force_authenticate(user=user)

        url = reverse("authors:authors-api-me")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(
            set(response.data.keys()),
            {"id", "username", "first_name", "last_name", "email"},
        )
        self.assertEqual(response.data["username"], "u1")
        self.assertNotEqual(response.data["username"], "u2")
