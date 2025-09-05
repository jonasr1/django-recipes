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
        self.assert_text_in_body(f"You are logged in with {user.username}.")

    def test_login_create_rejects_non_post_requests(self) -> None:
        self.open_page("authors:login_create")
        self.assert_text_in_body("Not Found")

    def test_login_shows_error_message_is_invalid(self) -> None:
        # User opens login page
        self.open_page("authors:login")
        # User sees login form
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        # And try to send empty values
        self.get_by_placeholder(form, "Type your username").send_keys("")
        self.get_by_placeholder(form, "Type your password").send_keys("")
        form.submit()
        # You see an error message on the screen
        self.assert_text_in_body("Invalid username or password")

    def test_login_shows_error_message_with_invalid_credentials(self) -> None:
        # User opens login page
        self.open_page("authors:login")
        # User sees login form
        form = self.browser.find_element(By.CLASS_NAME, "main-form")
        # And tries to send values ​​with data that doesn't match
        self.get_by_placeholder(form, "Type your username").send_keys("invalid_user")
        self.get_by_placeholder(form, "Type your password").send_keys("invalid_password")  # noqa: E501
        form.submit()
        # You see an error message on the screen
        self.assert_text_in_body("Invalid credentials")
