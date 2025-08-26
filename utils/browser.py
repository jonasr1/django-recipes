from pathlib import Path

from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = "chromedriver"
CHROMEDRIVER_PATH = ROOT_PATH / "bin" / CHROMEDRIVER_NAME


def make_chrome_browser(*options: str) -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    if selenium_headless := config("SELENIUM_HEADLESS", default=""):
        chrome_options.add_argument(selenium_headless)
    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


if __name__ == "__main__":
    browser = make_chrome_browser()
    browser.get("http://www.udemy.com/")
    browser.quit()
