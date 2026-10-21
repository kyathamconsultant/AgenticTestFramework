"""
Order Confirmation Page Object Model for SauceDemo application
"""
from pages.base_page import BasePage
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


class OrderConfirmationPage(BasePage):
    """Order confirmation page for SauceDemo"""

    # Locators
    CONFIRMATION_CONTAINER = ".checkout_complete_container"
    CONFIRMATION_MESSAGE = ".complete-header"
    CONFIRMATION_TEXT = ".complete-text"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"
    PONY_EXPRESS = ".pony_express"

    def __init__(self, page):
        """Initialize order confirmation page"""
        super().__init__(page)

    def wait_for_confirmation_page(self):
        """Wait for order confirmation page to load"""
        self.wait_for_element(self.CONFIRMATION_CONTAINER)
        logger.info("Order confirmation page loaded")

    def get_confirmation_message(self):
        """Get confirmation message"""
        try:
            message = self.get_text(self.CONFIRMATION_MESSAGE)
            logger.info(f"Confirmation message: {message}")
            return message
        except Exception as e:
            logger.error(f"Failed to get confirmation message: {str(e)}")
            return None

    def get_confirmation_text(self):
        """Get confirmation details text"""
        try:
            text = self.get_text(self.CONFIRMATION_TEXT)
            logger.info(f"Confirmation text: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get confirmation text: {str(e)}")
            return None

    def is_order_confirmed(self):
        """Check if order is confirmed"""
        is_visible = self.is_element_visible(self.CONFIRMATION_CONTAINER)
        logger.info(f"Order confirmed: {is_visible}")
        return is_visible

    def click_back_home(self):
        """Click back to home button"""
        logger.info("Clicking back to home button")
        return self.click_element(self.BACK_HOME_BUTTON)

    def take_confirmation_screenshot(self):
        """Take screenshot of confirmation page"""
        return self.take_screenshot("order_confirmation_page")
