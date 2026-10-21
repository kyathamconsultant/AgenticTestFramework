"""
Products Page Object Model for SauceDemo application
"""
from pages.base_page import BasePage
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


class ProductsPage(BasePage):
    """Products page for SauceDemo"""

    # Locators
    INVENTORY_CONTAINER = ".inventory_container"
    PRODUCTS_LIST = ".inventory_list"
    PRODUCT_ITEM = ".inventory_item"
    PRODUCT_NAME = ".inventory_item_name"
    PRODUCT_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "button[data-test*='add-to-cart']"
    REMOVE_BUTTON = "button[data-test*='remove']"
    SORT_DROPDOWN = "[data-test='product_sort_container']"
    CART_LINK = "a[data-test='shopping_cart_link']"
    CART_BADGE = ".shopping_cart_badge"
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    PRODUCT_TITLE_PAGE = ".title"

    def __init__(self, page):
        """Initialize products page"""
        super().__init__(page)

    def wait_for_products_page(self):
        """Wait for products page to load"""
        self.wait_for_element(self.INVENTORY_CONTAINER)
        logger.info("Products page loaded")

    def get_all_products(self):
        """Get all products on the page"""
        try:
            products = self.page.locator(self.PRODUCT_ITEM).all()
            logger.info(f"Found {len(products)} products")
            return products
        except Exception as e:
            logger.error(f"Failed to get products: {str(e)}")
            return []

    def get_product_count(self):
        """Get count of products displayed"""
        count = self.get_all_elements_count(self.PRODUCT_ITEM)
        logger.info(f"Product count: {count}")
        return count

    def get_product_names(self):
        """Get all product names"""
        try:
            products = self.page.locator(self.PRODUCT_NAME).all()
            names = [product.inner_text() for product in products]
            logger.info(f"Product names: {names}")
            return names
        except Exception as e:
            logger.error(f"Failed to get product names: {str(e)}")
            return []

    def get_product_prices(self):
        """Get all product prices"""
        try:
            prices = self.page.locator(self.PRODUCT_PRICE).all()
            price_values = [price.inner_text() for price in prices]
            logger.info(f"Product prices: {price_values}")
            return price_values
        except Exception as e:
            logger.error(f"Failed to get product prices: {str(e)}")
            return []

    def add_product_to_cart(self, product_name):
        """Add product to cart by name"""
        try:
            logger.info(f"Adding product to cart: {product_name}")
            # Find product and click add to cart button
            product = self.page.locator(
                f"text={product_name} >> ../.. >> button[data-test*='add-to-cart']"
            )
            product.click()
            logger.info(f"Product {product_name} added to cart")
            return True
        except Exception as e:
            logger.error(f"Failed to add product {product_name} to cart: {str(e)}")
            return False

    def add_all_products_to_cart(self):
        """Add all products to cart"""
        try:
            buttons = self.page.locator(self.ADD_TO_CART_BUTTON).all()
            for button in buttons:
                button.click()
            logger.info(f"Added {len(buttons)} products to cart")
            return True
        except Exception as e:
            logger.error(f"Failed to add all products to cart: {str(e)}")
            return False

    def remove_product_from_cart(self, product_name):
        """Remove product from cart by name"""
        try:
            logger.info(f"Removing product from cart: {product_name}")
            product = self.page.locator(
                f"text={product_name} >> ../.. >> button[data-test*='remove']"
            )
            product.click()
            logger.info(f"Product {product_name} removed from cart")
            return True
        except Exception as e:
            logger.error(f"Failed to remove product {product_name}: {str(e)}")
            return False

    def sort_products(self, sort_option):
        """Sort products by selected option"""
        try:
            logger.info(f"Sorting products by: {sort_option}")
            self.select_dropdown_option(self.SORT_DROPDOWN, sort_option)
            logger.info(f"Products sorted by: {sort_option}")
            return True
        except Exception as e:
            logger.error(f"Failed to sort products: {str(e)}")
            return False

    def get_cart_item_count(self):
        """Get count of items in cart badge"""
        try:
            if self.is_element_visible(self.CART_BADGE, timeout=2):
                count = self.get_text(self.CART_BADGE)
                logger.info(f"Cart item count: {count}")
                return int(count)
            else:
                logger.info("Cart is empty")
                return 0
        except Exception as e:
            logger.error(f"Failed to get cart count: {str(e)}")
            return 0

    def click_cart_link(self):
        """Click cart link"""
        logger.info("Clicking cart link")
        return self.click_element(self.CART_LINK)

    def go_to_cart(self):
        """Navigate to cart"""
        self.click_cart_link()
        logger.info("Navigated to cart")

    def click_product(self, product_name):
        """Click on product to view details"""
        try:
            logger.info(f"Clicking product: {product_name}")
            self.page.click(f"text={product_name}")
            logger.info(f"Opened product: {product_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to click product {product_name}: {str(e)}")
            return False

    def is_products_page_displayed(self):
        """Check if products page is displayed"""
        is_visible = self.is_element_visible(self.INVENTORY_CONTAINER)
        logger.info(f"Products page displayed: {is_visible}")
        return is_visible

    def open_menu(self):
        """Open side menu"""
        logger.info("Opening menu")
        return self.click_element(self.MENU_BUTTON)

    def logout(self):
        """Logout from menu"""
        logger.info("Logging out")
        self.open_menu()
        self.click_element(self.LOGOUT_LINK)
        logger.info("Logged out")

    def take_products_screenshot(self):
        """Take screenshot of products page"""
        return self.take_screenshot("products_page")
