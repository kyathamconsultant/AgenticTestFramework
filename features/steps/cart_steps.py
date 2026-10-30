"""
Step definitions for cart feature
"""
from behave import when, then, step
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utilities.logger_utils import get_logger
from utilities.screenshot_utils import ScreenshotUtils

logger = get_logger(__name__)


@step('I click on the cart link')
def step_click_cart_link(context):
    """Click on cart link"""
    products_page = context.products_page
    products_page.click_cart_link()
    cart_page = CartPage(context.browser)
    cart_page.wait_for_cart_page()
    context.cart_page = cart_page
    logger.info("Navigated to cart page")


@then('I should be on the cart page')
def step_verify_on_cart_page(context):
    """Verify user is on cart page"""
    cart_page = context.cart_page
    assert cart_page.is_cart_page_displayed(), "Cart page not displayed"
    ScreenshotUtils.take_screenshot(context.browser, "cart_page")
    logger.info("User is on cart page")


@then('Cart should be empty')
def step_verify_cart_empty(context):
    """Verify cart is empty"""
    cart_page = context.cart_page
    assert cart_page.is_cart_empty(), "Cart is not empty"
    logger.info("Cart is empty")


@then('Cart should contain "{expected_count}" item')
@then('Cart should contain "{expected_count}" items')
def step_verify_cart_item_count(context, expected_count):
    """Verify cart contains expected number of items"""
    cart_page = context.cart_page
    actual_count = cart_page.get_cart_item_count()
    assert actual_count == int(expected_count), \
        f"Expected {expected_count} items, but found {actual_count}"
    logger.info(f"Cart contains {actual_count} items")


@then('Item "{product_name}" should be in cart')
def step_verify_item_in_cart(context, product_name):
    """Verify specific item is in cart"""
    cart_page = context.cart_page
    items = cart_page.get_cart_item_names()
    assert product_name in items, \
        f"Product {product_name} not found in cart. Items: {items}"
    logger.info(f"Product {product_name} found in cart")


@when('I remove item "{product_name}" from cart')
def step_remove_item_from_cart(context, product_name):
    """Remove item from cart"""
    cart_page = context.cart_page
    assert cart_page.remove_item_from_cart(product_name), \
        f"Failed to remove {product_name} from cart"
    logger.info(f"Removed {product_name} from cart")


@when('I remove all items from cart')
def step_remove_all_items(context):
    """Remove all items from cart"""
    cart_page = context.cart_page
    assert cart_page.remove_all_items_from_cart(), "Failed to remove all items"
    logger.info("Removed all items from cart")


@when('I click continue shopping button')
def step_click_continue_shopping(context):
    """Click continue shopping button"""
    cart_page = context.cart_page
    assert cart_page.click_continue_shopping(), "Failed to click continue shopping"
    from pages.products_page import ProductsPage
    products_page = ProductsPage(context.browser)
    products_page.wait_for_products_page()
    context.products_page = products_page
    logger.info("Clicked continue shopping - back to products page")


@then('Cart total should be calculated correctly')
def step_verify_cart_total(context):
    """Verify cart total is calculated correctly"""
    cart_page = context.cart_page
    total = cart_page.calculate_total_price()
    assert total > 0, "Cart total is not calculated"
    logger.info(f"Cart total calculated: ${total:.2f}")


@step('I click checkout button')
def step_click_checkout_button(context):
    """Click checkout button"""
    cart_page = context.cart_page
    assert cart_page.click_checkout(), "Failed to click checkout button"
    checkout_page = CheckoutPage(context.browser)
    checkout_page.wait_for_checkout_page()
    context.checkout_page = checkout_page
    logger.info("Navigated to checkout page")


@then('Checkout button should be visible')
def step_verify_checkout_button_visible(context):
    """Verify checkout button is visible"""
    cart_page = context.cart_page
    assert cart_page.is_checkout_button_visible(), "Checkout button not visible"
    logger.info("Checkout button is visible")


@then('I should be on the checkout page')
def step_verify_on_checkout_page(context):
    """Verify user is on checkout page"""
    checkout_page = context.checkout_page
    assert checkout_page.is_checkout_page_displayed(), "Checkout page not displayed"
    ScreenshotUtils.take_screenshot(context.browser, "checkout_page")
    logger.info("User is on checkout page")
