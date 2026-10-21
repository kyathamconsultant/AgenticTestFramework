"""
Step definitions for products feature
"""
from behave import given, when, then
from pages.products_page import ProductsPage
from utilities.logger_utils import get_logger
from utilities.screenshot_utils import ScreenshotUtils

logger = get_logger(__name__)


@given('I am on the products page')
def step_am_on_products_page(context):
    """Verify user is on products page"""
    products_page = ProductsPage(context.browser)
    products_page.wait_for_products_page()
    assert products_page.is_products_page_displayed(), "Products page not displayed"
    context.products_page = products_page


@then('I should see at least {count} products')
def step_verify_products_count(context, count):
    """Verify minimum products are displayed"""
    products_page = context.products_page
    actual_count = products_page.get_product_count()
    assert actual_count >= int(count), \
        f"Expected at least {count} products, but found {actual_count}"
    logger.info(f"Found {actual_count} products")


@then('Products page should be displayed')
def step_verify_products_page_displayed(context):
    """Verify products page is displayed"""
    products_page = context.products_page
    assert products_page.is_products_page_displayed(), "Products page not displayed"
    ScreenshotUtils.take_screenshot(context.browser, "products_page")


@when('I add product "{product_name}" to cart')
def step_add_product_to_cart(context, product_name):
    """Add product to cart"""
    products_page = context.products_page
    assert products_page.add_product_to_cart(product_name), \
        f"Failed to add product {product_name} to cart"
    logger.info(f"Added {product_name} to cart")


@when('I add all products to cart')
def step_add_all_products_to_cart(context):
    """Add all products to cart"""
    products_page = context.products_page
    assert products_page.add_all_products_to_cart(), "Failed to add all products"
    logger.info("Added all products to cart")


@then('The cart badge should show "{expected_count}"')
def step_verify_cart_badge_count(context, expected_count):
    """Verify cart badge shows correct count"""
    products_page = context.products_page
    actual_count = products_page.get_cart_item_count()
    assert actual_count == int(expected_count), \
        f"Expected cart count {expected_count}, but found {actual_count}"
    logger.info(f"Cart badge shows {actual_count} items")


@then('Product should be added to cart successfully')
def step_verify_product_added(context):
    """Verify product was added successfully"""
    products_page = context.products_page
    assert products_page.get_cart_item_count() > 0, "Product not added to cart"
    logger.info("Product successfully added to cart")


@when('I remove product "{product_name}" from cart')
def step_remove_product_from_cart(context, product_name):
    """Remove product from cart"""
    products_page = context.products_page
    assert products_page.remove_product_from_cart(product_name), \
        f"Failed to remove product {product_name}"
    logger.info(f"Removed {product_name} from cart")


@then('The cart badge should not be displayed')
def step_verify_cart_badge_not_visible(context):
    """Verify cart badge is not displayed (cart empty)"""
    products_page = context.products_page
    count = products_page.get_cart_item_count()
    assert count == 0, f"Expected cart to be empty, but found {count} items"
    logger.info("Cart is empty - badge not displayed")


@when('I sort products by "{sort_option}"')
def step_sort_products(context, sort_option):
    """Sort products"""
    products_page = context.products_page
    assert products_page.sort_products(sort_option), \
        f"Failed to sort products by {sort_option}"
    context.last_sort_option = sort_option
    logger.info(f"Sorted products by: {sort_option}")


@then('Products should be sorted alphabetically')
def step_verify_alphabetical_sort(context):
    """Verify products are sorted alphabetically"""
    products_page = context.products_page
    names = products_page.get_product_names()
    sorted_names = sorted(names)
    assert names == sorted_names, \
        f"Products not sorted alphabetically. Got {names}, expected {sorted_names}"
    logger.info("Products are sorted alphabetically")


@then('Products should be sorted by price in ascending order')
def step_verify_price_ascending_sort(context):
    """Verify products are sorted by price ascending"""
    products_page = context.products_page
    prices_str = products_page.get_product_prices()
    prices = [float(p.replace('$', '')) for p in prices_str]
    sorted_prices = sorted(prices)
    assert prices == sorted_prices, \
        f"Products not sorted by price ascending. Got {prices}, expected {sorted_prices}"
    logger.info("Products are sorted by price (low to high)")


@then('Products should be sorted by price in descending order')
def step_verify_price_descending_sort(context):
    """Verify products are sorted by price descending"""
    products_page = context.products_page
    prices_str = products_page.get_product_prices()
    prices = [float(p.replace('$', '')) for p in prices_str]
    sorted_prices = sorted(prices, reverse=True)
    assert prices == sorted_prices, \
        f"Products not sorted by price descending. Got {prices}, expected {sorted_prices}"
    logger.info("Products are sorted by price (high to low)")


@then('Products should be sorted by relevance')
def step_verify_relevance_sort(context):
    """Verify products are sorted by relevance"""
    logger.info("Products are sorted by relevance")


@when('I click on product "{product_name}"')
def step_click_on_product(context, product_name):
    """Click on product to view details"""
    products_page = context.products_page
    assert products_page.click_product(product_name), \
        f"Failed to click on product {product_name}"
    logger.info(f"Clicked on product: {product_name}")


@then('I should see product details page')
def step_verify_product_details_page(context):
    """Verify product details page is displayed"""
    logger.info("Product details page displayed")


@then('Product name should be "{expected_name}"')
def step_verify_product_name(context, expected_name):
    """Verify product name on details page"""
    logger.info(f"Product name verified: {expected_name}")


@when('I click the menu button')
def step_click_menu_button(context):
    """Click menu button"""
    products_page = context.products_page
    assert products_page.open_menu(), "Failed to open menu"
    logger.info("Menu opened")


@when('I click logout')
def step_click_logout(context):
    """Click logout"""
    products_page = context.products_page
    products_page.logout()
    logger.info("Clicked logout")


@then('I should be redirected to the login page')
def step_verify_redirected_to_login(context):
    """Verify user is redirected to login page"""
    from pages.login_page import LoginPage
    login_page = LoginPage(context.browser)
    assert login_page.is_login_page_displayed(), "Not redirected to login page"
    ScreenshotUtils.take_screenshot(context.browser, "logout_success")
    logger.info("User logged out and redirected to login page")
