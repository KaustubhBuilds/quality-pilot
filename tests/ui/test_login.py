import allure
import pytest

from config.settings import settings
from pages.login_page import LoginPage


@allure.epic("Authentication")
@allure.feature("Login")
class TestLogin:
    @pytest.mark.smoke
    @pytest.mark.ui
    @allure.story("Valid login")
    @allure.title("Admin can log in with valid credentials")
    def test_valid_login(self, page):
        login = LoginPage(page)
        login.open()
        login.login(settings.ODOO_USER, settings.ODOO_PASSWORD)
        login.assert_logged_in()

    @pytest.mark.ui
    @allure.story("Invalid login")
    @allure.title("Wrong password shows error message")
    def test_invalid_password(self, page):
        login = LoginPage(page)
        login.open()
        login.login(settings.ODOO_USER, "wrong_password_999")
        login.assert_login_error()

    @pytest.mark.ui
    @allure.story("Invalid login")
    @allure.title("Empty email field shows HTML5 validation message")
    def test_empty_credentials(self, page):
        login = LoginPage(page)
        login.open()
        login.login("", "")
        validation_message = page.locator(login.EMAIL_FIELD).evaluate(
            "el => el.validationMessage"
        )
        assert validation_message != ""
