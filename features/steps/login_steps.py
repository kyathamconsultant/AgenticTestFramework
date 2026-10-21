"""
Step definitions for login feature
"""
from behave import given, when, then
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utilities.logger_utils import get_logger
from utilities.screenshot_utils import ScreenshotUtils

logger = get_logger(__name__)


@given('I navigate to the login page')
def step_navigate_to_login_page(context):
    """Navigate to login page"""
    login_page = LoginPage(context.browser)
    login_page.navigate_to_login()
    context.login_page = login_page


@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username"""
    login_page = context.login_page
    login_page.enter_username(username)


@when('I enter password "{password}"')
def step_enter_password(context, password):
    """Enter password"""
    login_page = context.login_page
    login_page.enter_password(password)


@when('I click the login button')
def step_click_login_button(context):
    """Click login button"""
    login_page = context.login_page
    login_page.click_login_button()


@given('I login with username "{username}" and password "{password}"')
def step_login_with_credentials(context, username, password):
    """Login with credentials"""
    login_page = context.login_page
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login_button()
    logger.info(f"Logged in with user: {username}")


@then('I should be redirected to the products page')
def step_verify_products_page(context):
    """Verify user is on products page"""
    products_page = ProductsPage(context.browser)
    assert products_page.is_products_page_displayed(), "Products page not displayed"
    context.products_page = products_page
    ScreenshotUtils.take_screenshot(context.browser, "successful_login")
    logger.info("User successfully redirected to products page")


@then('I should see an error message')
def step_verify_error_message(context):
    """Verify error message is displayed"""
    login_page = context.login_page
    assert login_page.is_error_message_displayed(), "Error message not displayed"
    ScreenshotUtils.take_screenshot(context.browser, "login_error")
    logger.info("Error message displayed on login page")


@then('The error message should contain "{expected_text}"')
def step_verify_error_message_text(context, expected_text):
    """Verify error message contains expected text"""
    login_page = context.login_page
    error_text = login_page.get_error_message()
    assert expected_text.lower() in error_text.lower(), \
        f"Expected '{expected_text}' in error message, but got '{error_text}'"
    logger.info(f"Error message verified: {error_text}")
