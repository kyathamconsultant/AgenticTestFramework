"""
Cart Page Object Model for SauceDemo application
"""
from pages.base_page import BasePage
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    """Shopping cart page for SauceDemo"""

    # Locators
    CART_CONTAINER = ".cart_container"
    CART_LIST = ".cart_list"
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    CART_QUANTITY = ".cart_quantity"
    REMOVE_BUTTON = "button[data-test*='remove']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    EMPTY_CART_MESSAGE = ".empty_message"

    def __init__(self, page):
        """Initialize cart page"""
        super().__init__(page)

    def wait_for_cart_page(self):
        """Wait for cart page to load"""
        self.wait_for_element(self.CART_CONTAINER)
        logger.info("Cart page loaded")

    def get_cart_items(self):
        """Get all items in cart"""
        try:
            items = self.page.locator(self.CART_ITEM).all()
            logger.info(f"Found {len(items)} items in cart")
            return items
        except Exception as e:
            logger.error(f"Failed to get cart items: {str(e)}")
            return []

    def get_cart_item_count(self):
        """Get count of items in cart"""
        count = self.get_all_elements_count(self.CART_ITEM)
        logger.info(f"Cart item count: {count}")
        return count

    def get_cart_item_names(self):
        """Get all cart item names"""
        try:
            items = self.page.locator(self.CART_ITEM_NAME).all()
            names = [item.inner_text() for item in items]
            logger.info(f"Cart item names: {names}")
            return names
        except Exception as e:
            logger.error(f"Failed to get cart item names: {str(e)}")
            return []

    def get_cart_item_prices(self):
        """Get all cart item prices"""
        try:
            prices = self.page.locator(self.CART_ITEM_PRICE).all()
            price_values = [price.inner_text() for price in prices]
            logger.info(f"Cart item prices: {price_values}")
            return price_values
        except Exception as e:
            logger.error(f"Failed to get cart item prices: {str(e)}")
            return []

    def remove_item_from_cart(self, product_name):
        """Remove item from cart by product name"""
        try:
            logger.info(f"Removing item from cart: {product_name}")
            item = self.page.locator(
                f"text={product_name} >> ../.. >> button[data-test*='remove']"
            )
            item.click()
            logger.info(f"Item {product_name} removed from cart")
            return True
        except Exception as e:
            logger.error(f"Failed to remove item {product_name}: {str(e)}")
            return False

    def remove_all_items_from_cart(self):
        """Remove all items from cart"""
        try:
            buttons = self.page.locator(self.REMOVE_BUTTON).all()
            for button in buttons:
                button.click()
            logger.info(f"Removed all {len(buttons)} items from cart")
            return True
        except Exception as e:
            logger.error(f"Failed to remove all items: {str(e)}")
            return False

    def click_continue_shopping(self):
        """Click continue shopping button"""
        logger.info("Clicking continue shopping button")
        return self.click_element(self.CONTINUE_SHOPPING_BUTTON)

    def click_checkout(self):
        """Click checkout button"""
        logger.info("Clicking checkout button")
        return self.click_element(self.CHECKOUT_BUTTON)

    def is_cart_empty(self):
        """Check if cart is empty"""
        try:
            is_empty = self.is_element_visible(self.EMPTY_CART_MESSAGE, timeout=2)
            logger.info(f"Cart is empty: {is_empty}")
            return is_empty
        except Exception as e:
            logger.info("Cart is not empty")
            return False

    def is_cart_page_displayed(self):
        """Check if cart page is displayed"""
        is_visible = self.is_element_visible(self.CART_CONTAINER)
        logger.info(f"Cart page displayed: {is_visible}")
        return is_visible

    def is_checkout_button_visible(self):
        """Check if checkout button is visible"""
        return self.is_element_visible(self.CHECKOUT_BUTTON)

    def calculate_total_price(self):
        """Calculate total price of items in cart"""
        try:
            prices = self.get_cart_item_prices()
            total = 0
            for price in prices:
                # Remove $ and convert to float
                price_value = float(price.replace('$', ''))
                total += price_value
            logger.info(f"Total price: ${total:.2f}")
            return total
        except Exception as e:
            logger.error(f"Failed to calculate total: {str(e)}")
            return 0

    def take_cart_screenshot(self):
        """Take screenshot of cart page"""
        return self.take_screenshot("cart_page")
