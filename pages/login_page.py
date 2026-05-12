import allure
from playwright.sync_api import Page

from config.settings import settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page object for the Odoo login page.
    URL: /web/login
    Inherits all common actions from BasePage.
    """

    # Selectors found using Playwright Inspector
    EMAIL_FIELD = '[id="login"]'
    PASSWORD_FIELD = '[id="password"]'
    LOGIN_BUTTON = '[type="submit"]'
    USER_MENU = ".o_user_menu"
    ERROR_MESSAGE = ".alert.alert-danger"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Open Odoo login page")
    def open(self):
        self.navigate(f"{settings.BASE_URL}/web/login")

    @allure.step("Login with username: {username}")
    def login(self, username: str, password: str):
        self.fill(self.EMAIL_FIELD, username)
        self.fill(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Assert login was successful")
    def assert_logged_in(self):
        self.assert_visible(self.USER_MENU)

    @allure.step("Assert login error is shown")
    def assert_login_error(self):
        self.assert_visible(self.ERROR_MESSAGE)
