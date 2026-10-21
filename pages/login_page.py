"""
Login Page Object Model for SauceDemo application
"""
from pages.base_page import BasePage
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Login page for SauceDemo"""

    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    LOGIN_CONTAINER = ".login_container"

    def __init__(self, page):
        """Initialize login page"""
        super().__init__(page)

    def navigate_to_login(self):
        """Navigate to login page"""
        self.navigate_to(self.base_url)
        self.wait_for_element(self.LOGIN_CONTAINER)
        logger.info("Navigated to login page")

    def enter_username(self, username):
        """Enter username"""
        logger.info(f"Entering username: {username}")
        return self.fill_input(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Enter password"""
        logger.info("Entering password")
        return self.fill_input(self.PASSWORD_INPUT, password)

    def click_login_button(self):
        """Click login button"""
        logger.info("Clicking login button")
        return self.click_element(self.LOGIN_BUTTON)

    def login(self, username, password):
        """Perform login with username and password"""
        logger.info(f"Logging in with user: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self):
        """Get error message if login fails"""
        try:
            error_text = self.get_text(self.ERROR_MESSAGE)
            logger.warning(f"Login error: {error_text}")
            return error_text
        except Exception as e:
            logger.info("No error message found")
            return None

    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        is_visible = self.is_element_visible(self.ERROR_MESSAGE, timeout=2)
        logger.info(f"Error message displayed: {is_visible}")
        return is_visible

    def is_login_page_displayed(self):
        """Check if login page is displayed"""
        is_visible = self.is_element_visible(self.LOGIN_CONTAINER)
        logger.info(f"Login page displayed: {is_visible}")
        return is_visible

    def is_username_field_visible(self):
        """Check if username field is visible"""
        return self.is_element_visible(self.USERNAME_INPUT)

    def is_password_field_visible(self):
        """Check if password field is visible"""
        return self.is_element_visible(self.PASSWORD_INPUT)

    def is_login_button_visible(self):
        """Check if login button is visible"""
        return self.is_element_visible(self.LOGIN_BUTTON)

    def take_login_screenshot(self):
        """Take screenshot of login page"""
        return self.take_screenshot("login_page")
