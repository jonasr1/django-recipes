from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from recipes.tests.test_recipe_base import RecipeMixin
from tests.functional_tests.recipes.base import RecipeBasePageFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBasePageFunctionalTest, RecipeMixin):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("No recipes found here 🥲", body.text)

    @patch("recipes.views.PER_PAGE", new=2)
    def test_recipe_search_input_can_find_correct_recipes(self) -> None:
        recipes = self.make_recipe_in_batch()
        title_needed = "This is what i need"
        recipes[0].title = title_needed
        recipes[0].save()
        # user opens the page
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Search for a recipe"]')
        # Click this input and enter the search term
        # to find the recipe with the desired title
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)
        # The user sees what they were looking for on the page
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, "main-content-list").text,
        )

    @patch("recipes.views.PER_PAGE", new=2)
    def test_recipe_home_page_pagination(self) -> None:
        self.make_recipe_in_batch()
        # user opens the page
        self.browser.get(self.live_server_url)
        # You see that there is a pagination and click on page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]',
        )
        page2.click()
        # See that there are 2 more recipes on page 2
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, "recipe")), 2)
