"""
Checkout Page Object Model for SauceDemo application
"""
from pages.base_page import BasePage
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


class CheckoutPage(BasePage):
    """Checkout page for SauceDemo"""

    # Checkout Step One Locators
    CHECKOUT_CONTAINER = ".checkout_container"
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    ERROR_MESSAGE = "[data-test='error']"

    # Checkout Step Two Locators
    CHECKOUT_SUMMARY_CONTAINER = ".checkout_summary_container"
    ITEM_TOTAL = "[data-test='subtotal-label']"
    TAX_TOTAL = "[data-test='tax-label']"
    TOTAL_PRICE = "[data-test='total-label']"
    FINISH_BUTTON = "[data-test='finish']"
    CANCEL_BUTTON = "[data-test='cancel']"

    def __init__(self, page):
        """Initialize checkout page"""
        super().__init__(page)

    def wait_for_checkout_page(self):
        """Wait for checkout page to load"""
        self.wait_for_element(self.CHECKOUT_CONTAINER)
        logger.info("Checkout page loaded")

    # Step One - Information
    def enter_first_name(self, first_name):
        """Enter first name"""
        logger.info(f"Entering first name: {first_name}")
        return self.fill_input(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        """Enter last name"""
        logger.info(f"Entering last name: {last_name}")
        return self.fill_input(self.LAST_NAME_INPUT, last_name)

    def enter_postal_code(self, postal_code):
        """Enter postal code"""
        logger.info(f"Entering postal code: {postal_code}")
        return self.fill_input(self.POSTAL_CODE_INPUT, postal_code)

    def fill_checkout_information(self, first_name, last_name, postal_code):
        """Fill all checkout information"""
        logger.info("Filling checkout information")
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)

    def click_continue(self):
        """Click continue button"""
        logger.info("Clicking continue button")
        return self.click_element(self.CONTINUE_BUTTON)

    def proceed_to_checkout_step_two(self, first_name, last_name, postal_code):
        """Proceed to checkout step two"""
        logger.info("Proceeding to checkout step two")
        self.fill_checkout_information(first_name, last_name, postal_code)
        self.click_continue()

    def get_error_message(self):
        """Get error message if validation fails"""
        try:
            error_text = self.get_text(self.ERROR_MESSAGE)
            logger.warning(f"Checkout error: {error_text}")
            return error_text
        except Exception as e:
            logger.info("No error message found")
            return None

    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        is_visible = self.is_element_visible(self.ERROR_MESSAGE, timeout=2)
        logger.info(f"Error message displayed: {is_visible}")
        return is_visible

    # Step Two - Summary
    def wait_for_checkout_summary(self):
        """Wait for checkout summary page"""
        self.wait_for_element(self.CHECKOUT_SUMMARY_CONTAINER)
        logger.info("Checkout summary page loaded")

    def get_item_total(self):
        """Get item total"""
        try:
            total_text = self.get_text(self.ITEM_TOTAL)
            # Extract price value
            price = float(total_text.split('$')[1])
            logger.info(f"Item total: ${price}")
            return price
        except Exception as e:
            logger.error(f"Failed to get item total: {str(e)}")
            return 0

    def get_tax_total(self):
        """Get tax total"""
        try:
            tax_text = self.get_text(self.TAX_TOTAL)
            # Extract tax value
            price = float(tax_text.split('$')[1])
            logger.info(f"Tax total: ${price}")
            return price
        except Exception as e:
            logger.error(f"Failed to get tax total: {str(e)}")
            return 0

    def get_final_total(self):
        """Get final total"""
        try:
            total_text = self.get_text(self.TOTAL_PRICE)
            # Extract total value
            price = float(total_text.split('$')[1])
            logger.info(f"Final total: ${price}")
            return price
        except Exception as e:
            logger.error(f"Failed to get final total: {str(e)}")
            return 0

    def click_finish(self):
        """Click finish button to complete order"""
        logger.info("Clicking finish button")
        return self.click_element(self.FINISH_BUTTON)

    def click_cancel(self):
        """Click cancel button"""
        logger.info("Clicking cancel button")
        return self.click_element(self.CANCEL_BUTTON)

    def is_checkout_page_displayed(self):
        """Check if checkout page is displayed"""
        is_visible = self.is_element_visible(self.CHECKOUT_CONTAINER)
        logger.info(f"Checkout page displayed: {is_visible}")
        return is_visible

    def is_finish_button_visible(self):
        """Check if finish button is visible"""
        return self.is_element_visible(self.FINISH_BUTTON)

    def take_checkout_screenshot(self):
        """Take screenshot of checkout page"""
        return self.take_screenshot("checkout_page")
