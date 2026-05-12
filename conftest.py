import allure
import pytest
from playwright.sync_api import sync_playwright

from config.settings import settings


@pytest.fixture(scope="session")
def browser_instance():
    """
    Session-scoped: browser starts ONCE for the entire test run.
    Starting a browser takes ~2 seconds. With 30 tests, session scope
    saves ~60 seconds compared to restarting the browser every test.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=settings.HEADLESS,
            slow_mo=settings.SLOW_MO,
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance):
    """
    Function-scoped: every test gets a FRESH browser context.
    This is test isolation one test's cookies, session, and
    storage never bleed into another test.
    """
    context = browser_instance.new_context(
        base_url=settings.BASE_URL,
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_in_page(page):
    """
    Pre-authenticated page fixture.
    Tests that need a logged-in state use this instead of 'page'.
    Login happens automatically before the test body runs.
    Avoids repeating login code in every single test.
    """
    from pages.login_page import LoginPage

    login = LoginPage(page)
    login.open()
    login.login(settings.ODOO_USER, settings.ODOO_PASSWORD)
    login.assert_logged_in()
    yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Runs automatically after every test.
    If a test fails, takes a screenshot and attaches it to Allure.
    You never have to manually add screenshot code to any test.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_fixture = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
        if page_fixture:
            allure.attach(
                page_fixture.screenshot(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
