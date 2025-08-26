import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import make_chrome_browser


class RecipeBasePageFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()

    def tearDown(self) -> None:
        self.browser.quit()

    def sleep(self, seconds: int = 5) -> None:
        time.sleep(seconds)
