import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from datetime import datetime
import os


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser name: chrome or firefox or edge")


@pytest.fixture(scope="function")
def setup(request):
    browser = request.config.getoption("--browser").lower()

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=ChromeService(), options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(service=FirefoxService(), options=options)

    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument('--headless')
        driver = webdriver.Edge(service=EdgeService(), options=options)

    else:
        raise ValueError(f"Browser '{browser}' is not supported. Use 'chrome', 'firefox' or 'edge'.")

    driver.maximize_window()
    yield driver
    driver.quit()


def pytest_exception_interact(node, call, report):
    if report.failed:
        driver = node.funcargs['setup']
        screenshot_name = datetime.now().strftime("screenshots/failure_%Y%m%d_%H%M%S.png")
        driver.save_screenshot(screenshot_name)
