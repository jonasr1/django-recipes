import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utils.browser import make_chrome_browser


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds: int = 5) -> None:
        time.sleep(seconds)

    def get_by_placeholder(self, form: WebElement, placeholder: str) -> WebElement:
        return form.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')

    def get_error(self, field_name: str) -> WebElement:
        return WebDriverWait(self.browser, 5).until(
            ec.presence_of_element_located((By.ID, f"id_{field_name}_error")),
        )

    def open_page(self, url_name: str) -> None:
        """Open a page using the Django URL name."""
        full_url = self.live_server_url + reverse(url_name)
        self.browser.get(full_url)
