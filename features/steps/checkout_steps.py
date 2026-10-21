"""
Step definitions for checkout feature
"""
from behave import when, then
from pages.checkout_page import CheckoutPage
from pages.order_confirmation_page import OrderConfirmationPage
from pages.products_page import ProductsPage
from utilities.logger_utils import get_logger
from utilities.screenshot_utils import ScreenshotUtils

logger = get_logger(__name__)


@then('I should be on the checkout summary page')
def step_verify_on_checkout_summary(context):
    """Verify user is on checkout summary page"""
    checkout_page = context.checkout_page
    checkout_page.wait_for_checkout_summary()
    assert checkout_page.is_checkout_page_displayed(), "Checkout summary page not displayed"
    ScreenshotUtils.take_screenshot(context.browser, "checkout_summary")
    logger.info("User is on checkout summary page")


@then('Order summary should be displayed')
def step_verify_order_summary_displayed(context):
    """Verify order summary is displayed"""
    checkout_page = context.checkout_page
    assert checkout_page.is_finish_button_visible(), "Order summary not displayed"
    logger.info("Order summary is displayed")


@when('I enter first name "{first_name}"')
def step_enter_first_name(context, first_name):
    """Enter first name"""
    checkout_page = context.checkout_page
    assert checkout_page.enter_first_name(first_name), f"Failed to enter first name: {first_name}"
    logger.info(f"Entered first name: {first_name}")


@when('I enter last name "{last_name}"')
def step_enter_last_name(context, last_name):
    """Enter last name"""
    checkout_page = context.checkout_page
    assert checkout_page.enter_last_name(last_name), f"Failed to enter last name: {last_name}"
    logger.info(f"Entered last name: {last_name}")


@when('I enter postal code "{postal_code}"')
def step_enter_postal_code(context, postal_code):
    """Enter postal code"""
    checkout_page = context.checkout_page
    assert checkout_page.enter_postal_code(postal_code), f"Failed to enter postal code: {postal_code}"
    logger.info(f"Entered postal code: {postal_code}")


@when('I click continue button')
def step_click_continue_button(context):
    """Click continue button"""
    checkout_page = context.checkout_page
    assert checkout_page.click_continue(), "Failed to click continue button"
    logger.info("Clicked continue button")


@then('I should see a checkout error message')
def step_verify_error_message(context):
    """Verify error message is displayed on checkout page"""
    checkout_page = context.checkout_page
    assert checkout_page.is_error_message_displayed(), "Error message not displayed"
    ScreenshotUtils.take_screenshot(context.browser, "checkout_error")
    logger.info("Error message displayed on checkout page")


@then('The checkout error message should contain "{expected_text}"')
def step_verify_error_message_text(context, expected_text):
    """Verify checkout error message contains expected text"""
    checkout_page = context.checkout_page
    error_text = checkout_page.get_error_message()
    assert expected_text.lower() in error_text.lower(), \
        f"Expected '{expected_text}' in error, but got '{error_text}'"
    logger.info(f"Error message verified: {error_text}")


@when('I click finish button')
def step_click_finish_button(context):
    """Click finish button"""
    checkout_page = context.checkout_page
    assert checkout_page.click_finish(), "Failed to click finish button"
    order_page = OrderConfirmationPage(context.browser)
    order_page.wait_for_confirmation_page()
    context.order_confirmation_page = order_page
    logger.info("Clicked finish button - navigating to order confirmation")


@then('I should see order confirmation message')
def step_verify_order_confirmation(context):
    """Verify order confirmation message"""
    order_page = context.order_confirmation_page
    assert order_page.is_order_confirmed(), "Order not confirmed"
    message = order_page.get_confirmation_message()
    assert "thank you" in message.lower(), f"Unexpected confirmation message: {message}"
    logger.info(f"Order confirmation message: {message}")


@then('Order should be confirmed successfully')
def step_verify_order_confirmed(context):
    """Verify order is confirmed"""
    order_page = context.order_confirmation_page
    assert order_page.is_order_confirmed(), "Order confirmation failed"
    ScreenshotUtils.take_screenshot(context.browser, "order_confirmed")
    logger.info("Order confirmed successfully")


@then('Item total should be displayed')
def step_verify_item_total_displayed(context):
    """Verify item total is displayed"""
    checkout_page = context.checkout_page
    total = checkout_page.get_item_total()
    assert total > 0, "Item total not displayed"
    logger.info(f"Item total displayed: ${total}")


@then('Tax should be calculated')
def step_verify_tax_calculated(context):
    """Verify tax is calculated"""
    checkout_page = context.checkout_page
    tax = checkout_page.get_tax_total()
    assert tax >= 0, "Tax not calculated"
    logger.info(f"Tax calculated: ${tax}")


@then('Final total should be displayed')
def step_verify_final_total_displayed(context):
    """Verify final total is displayed"""
    checkout_page = context.checkout_page
    total = checkout_page.get_final_total()
    assert total > 0, "Final total not displayed"
    logger.info(f"Final total displayed: ${total}")


@when('I click cancel button')
def step_click_cancel_button(context):
    """Click cancel button"""
    checkout_page = context.checkout_page
    assert checkout_page.click_cancel(), "Failed to click cancel button"
    from pages.products_page import ProductsPage
    products_page = ProductsPage(context.browser)
    products_page.wait_for_products_page()
    context.products_page = products_page
    logger.info("Clicked cancel - returned to products page")
