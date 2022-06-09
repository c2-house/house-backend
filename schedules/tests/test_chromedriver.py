from django.conf import settings
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service


def test_chromedriver_work():
    chromedriver_path = settings.CHROME_DRIVER_PATH
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(chromedriver_path)
    browser = Chrome(service=service, options=options)

    assert browser
