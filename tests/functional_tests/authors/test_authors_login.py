import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By

from tests.functional_tests.authors.base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self) -> None:
        password_string = "pass"  # noqa: S105
        user = User.objects.create_user(username="my_user", password=password_string)
        # User opens login page
        self.open_page("authors:login")
        # User sees login form
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        username_field = self.get_by_placeholder(form, "Type your username")
        password_field = self.get_by_placeholder(form, "Type your password")
        # User enters his username and password
        username_field.send_keys(user.username)
        password_field.send_keys(password_string)
        # User submits the form
        form.submit()
        # User sees successful login message and their name
        self.assertIn(
            f"You are logged in with {user.username}.",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )
