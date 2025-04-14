
import pytest
from pageobjects.login_page import LoginPage
from utilities.utils import read_properties

config = read_properties("utilities/config.properties")

@pytest.mark.parametrize("username,password,expected_result", [

    (config.get('DEFAULT', 'username'), config.get('DEFAULT', 'password'), "FHPLUS :: Employee"),  # valid credentials
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

    if expected_result == "FHPLUS :: Employee":
        assert expected_result in driver.title
    else:
        assert login_page.get_error_message() == expected_result
