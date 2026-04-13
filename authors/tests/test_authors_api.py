# ruff:noqa: S106
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthorAPITest(APITestCase):
    def get_create_user_payload(self) -> dict[str, str]:
        return {
            "username": "new_user",
            "first_name": "New",
            "last_name": "User",
            "email": "new_user@example.com",
            "password": "StrongPass1",
            "password2": "StrongPass1",
        }

    def test_author_api_create_user_returns_status_code_201(self) -> None:
        User = get_user_model()  # noqa: N806
        url = reverse("authors:authors-api-list")
        payload = self.get_create_user_payload()

        response = self.client.post(url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            set(response.data.keys()),
            {"id", "username", "first_name", "last_name", "email"},
        )
        self.assertNotIn("password", response.data)
        created_user = User.objects.get(username=payload["username"])
        self.assertTrue(created_user.check_password(payload["password"]))
        self.assertEqual(created_user.email, payload["email"])

    def test_author_api_create_user_returns_400_when_passwords_do_not_match(
        self,
    ) -> None:
        User = get_user_model()  # noqa: N806
        url = reverse("authors:authors-api-list")
        payload = self.get_create_user_payload()
        payload["password2"] = "StrongPass2"

        response = self.client.post(url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertIn("password2", response.data)
        self.assertFalse(User.objects.filter(username=payload["username"]).exists())

    def test_author_api_create_user_returns_400_when_email_already_exists(
        self,
    ) -> None:
        User = get_user_model()  # noqa: N806
        existing_user = self.get_create_user_payload()
        User.objects.create_user(
            username="existing_user",
            password=existing_user["password"],
            email=existing_user["email"],
        )
        url = reverse("authors:authors-api-list")
        payload = self.get_create_user_payload()
        payload["username"] = "another_user"

        response = self.client.post(url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("User e-mail is already in use", response.data["email"])

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

    def test_author_me_requires_authentication(self) -> None:
        url = reverse("authors:authors-api-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
