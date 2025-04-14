import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime


@pytest.fixture(scope="function")
def setup():
    options = Options()
    # options.add_argument('--headless')
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def pytest_exception_interact(node, call, report):
    if report.failed:
        driver = node.funcargs['setup']
        screenshot_name = datetime.now().strftime("screenshots/failure_%Y%m%d_%H%M%S.png")
        driver.save_screenshot(screenshot_name)
