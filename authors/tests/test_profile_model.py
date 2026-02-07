from django.contrib.auth import get_user_model
from django.test import TestCase

from authors.models import Profile


class ProfileModelTest(TestCase):
    def test_profile_str_returns_username(self) -> None:
        User = get_user_model()  # noqa: N806
        user = User.objects.create_user(username="user1", password="pass")  # noqa: S106
        profile, _created = Profile.objects.get_or_create(author=user)
        self.assertEqual(str(profile), "user1")
