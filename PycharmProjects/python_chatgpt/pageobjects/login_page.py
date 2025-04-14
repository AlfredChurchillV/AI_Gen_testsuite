
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "txtUserId")
        self.password_input = (By.ID, "txtPassword")

        self.error_message = (By.ID, "error")
        self.login_button = (By.ID, "btnLogin")
        # locators are added by alfred

    def login(self, username, password):
        self.driver.find_element(*self.username_input).clear()
        self.driver.find_element(*self.username_input).send_keys(username)

        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text
