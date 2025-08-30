from collections.abc import Callable
from uuid import uuid1

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from tests.functional_tests.authors.base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form: WebElement) -> None:
        fields = form.find_elements(By.TAG_NAME, "input")
        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)

    def get_by_placeholder(self, form: WebElement, placeholder: str) -> WebElement:
        return form.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')

    def get_error(self, field_name: str) -> WebElement:
        return WebDriverWait(self.browser, 5).until(
            ec.presence_of_element_located((By.ID, f"id_{field_name}_error")),
        )

    def form_field_test_with_callback(
        self, field_check: Callable[[WebElement], None],
    ) -> WebElement:
        self.browser.get(self.live_server_url + "/authors/register")
        form = self.browser.find_element(By.XPATH, "/html/body/div/main/div[2]/form")
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, "email").send_keys("dummy@gmail.com")
        field_check(form)
        return form

    def test_empty_first_name_error_message(self) -> None:
        def callback(form: WebElement) -> None:
            first_name_field = self.get_by_placeholder(form, "Ex.: John")
            first_name_field.send_keys(" ")
            form.submit()
            error_element = self.get_error("first_name")
            self.assertIn("Write your first name", error_element.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self) -> None:
        def callback(form: WebElement) -> None:
            last_name_field = self.get_by_placeholder(form, "Ex.: Doe")
            last_name_field.send_keys(" ")
            form.submit()
            error_element = self.get_error("last_name")
            self.assertIn("Write your last name", error_element.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self) -> None:
        def callback(form: WebElement) -> None:
            username_field = self.get_by_placeholder(form, "Your username")
            username_field.send_keys(" ")
            form.submit()
            error_element = self.get_error("username")
            self.assertIn("This field must not be empty", error_element.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self) -> None:
        def callback(form: WebElement) -> None:
            email_field = self.get_by_placeholder(form, "Your e-mail")
            email_field.send_keys(Keys.CONTROL + "a", Keys.DELETE)
            email_field.send_keys("email@invalid")
            form.submit()
            error_element = self.get_error("email")
            self.assertIn("Enter a valid email address.", error_element.text)
        self.form_field_test_with_callback(callback)

    def test_password_do_not_match(self) -> None:
        def callback(form: WebElement) -> None:
            password1_field = self.get_by_placeholder(form, "Type your password")
            password2_field = self.get_by_placeholder(form, "Repeat your password")
            password1_field.send_keys("P@ssw0rd")
            password2_field.send_keys("P@ssw0rd_Different")
            form.submit()
            error_element = self.get_error("password")
            self.assertIn("Password and password2 must be equal", error_element.text)
        self.form_field_test_with_callback(callback)

    def test_register_with_valid_data_shows_success_message(self) -> None:
        self.browser.get(self.live_server_url + "/authors/register")
        form = self.browser.find_element(By.XPATH, "/html/body/div/main/div[2]/form")
        unique_username = f"user_{uuid1().hex[:8]}"
        unique_email = f"{unique_username}@valid.com"

        fields = {
            "Ex.: John": "First Name",
            "Ex.: Doe": "Last Name",
            "Your username": unique_username,
            "Your e-mail": unique_email,
            "Type your password": "P@ssw0rd",
            "Repeat your password": "P@ssw0rd",
        }
        for placeholder, value in fields.items():
            self.get_by_placeholder(form, placeholder).send_keys(value)
        form.submit()
        self.assertIn(
            "Your user is created, please log in.",
            self.browser.find_element(By.TAG_NAME, "body").text,
        )
