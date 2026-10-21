"""
Environment setup for Behave tests
Handles browser initialization and teardown
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
from config.config import Config
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


def before_all(context):
    """Setup before all tests"""
    logger.info("=" * 80)
    logger.info("STARTING TEST SUITE")
    logger.info("=" * 80)
    Config.ensure_directories()


def before_scenario(context, scenario):
    """Setup before each scenario"""
    logger.info("")
    logger.info(f"Starting scenario: {scenario.name}")
    logger.info("-" * 80)

    # Initialize Playwright
    context.playwright = sync_playwright().start()

    # Select browser
    if Config.BROWSER_TYPE == "firefox":
        browser = context.playwright.firefox.launch(
            headless=Config.HEADLESS,
            slow_mo=Config.SLOW_MO
        )
    elif Config.BROWSER_TYPE == "webkit":
        browser = context.playwright.webkit.launch(
            headless=Config.HEADLESS,
            slow_mo=Config.SLOW_MO
        )
    else:  # chromium (default)
        browser = context.playwright.chromium.launch(
            headless=Config.HEADLESS,
            slow_mo=Config.SLOW_MO
        )

    # Create browser context
    context.browser_instance = browser
    context.browser = browser.new_page(
        viewport={
            "width": Config.VIEWPORT_WIDTH,
            "height": Config.VIEWPORT_HEIGHT
        }
    )

    logger.info(f"Browser initialized: {Config.BROWSER_TYPE}")
    logger.info(f"Headless mode: {Config.HEADLESS}")
    logger.info(f"Viewport: {Config.VIEWPORT_WIDTH}x{Config.VIEWPORT_HEIGHT}")


def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    # Take screenshot on failure
    if scenario.status == "failed":
        logger.error(f"Scenario FAILED: {scenario.name}")
        scenario_name = scenario.name.replace(" ", "_").lower()
        from utilities.screenshot_utils import ScreenshotUtils
        screenshot_path = ScreenshotUtils.take_screenshot_on_failure(
            context.browser,
            scenario_name
        )
        if screenshot_path:
            ScreenshotUtils.attach_screenshot_to_allure(screenshot_path)
    else:
        logger.info(f"Scenario PASSED: {scenario.name}")

    # Close browser
    if context.browser:
        context.browser.close()

    # Close browser instance
    if hasattr(context, 'browser_instance'):
        context.browser_instance.close()

    # Stop playwright
    if hasattr(context, 'playwright'):
        context.playwright.stop()

    logger.info("-" * 80)


def after_all(context):
    """Cleanup after all tests"""
    logger.info("=" * 80)
    logger.info("TEST SUITE COMPLETED")
    logger.info("=" * 80)
