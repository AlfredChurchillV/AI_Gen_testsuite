import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from datetime import datetime

# Folder Structure
os.makedirs("pageobjects", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)
os.makedirs("testcases", exist_ok=True)
os.makedirs("utilities", exist_ok=True)

# pageobjects/login_page.py
with open("pageobjects/login_page.py", "w") as f:
    f.write('''
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login")
        self.error_message = (By.ID, "error")  # Assuming error message element ID

    def login(self, username, password):
        self.driver.find_element(*self.username_input).clear()
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text
''')

# utilities/utils.py
with open("utilities/utils.py", "w") as f:
    f.write('''
import configparser

def read_properties(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config
''')

# config.properties
with open("utilities/config.properties", "w") as f:
    f.write('''
[DEFAULT]
url = https://example.com/login
username = testuser
password = testpass
''')

# conftest.py for setup and teardown
with open("conftest.py", "w") as f:
    f.write('''
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime

@pytest.fixture(scope="function")
def setup():
    options = Options()
    options.add_argument('--headless')
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
''')

# testcases/test_login.py
with open("testcases/test_login.py", "w") as f:
    f.write('''
import pytest
from pageobjects.login_page import LoginPage
from utilities.utils import read_properties

config = read_properties("utilities/config.properties")

@pytest.mark.parametrize("username,password,expected_result", [
    (config.get('DEFAULT', 'username'), config.get('DEFAULT', 'password'), "Dashboard"),  # valid credentials
    ("invalidUser", config.get('DEFAULT', 'password'), "Invalid username or password"),   # invalid username
    (config.get('DEFAULT', 'username'), "wrongpass", "Invalid username or password"),      # invalid password
    ("", config.get('DEFAULT', 'password'), "Username is required"),                      # empty username
    (config.get('DEFAULT', 'username'), "", "Password is required"),                      # empty password
    ("", "", "Username and Password are required")                                       # both empty
])
def test_login_cases(setup, username, password, expected_result):
    driver = setup
    driver.get(config.get('DEFAULT', 'url'))
    login_page = LoginPage(driver)
    login_page.login(username, password)

    if expected_result == "Dashboard":
        assert expected_result in driver.title
    else:
        assert login_page.get_error_message() == expected_result
''')

# pytest.ini for custom output
with open("pytest.ini", "w") as f:
    f.write('''
[pytest]
addopts = --html=reports/report.html --self-contained-html
''')
