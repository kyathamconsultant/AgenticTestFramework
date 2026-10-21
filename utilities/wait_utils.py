"""
Wait utilities for handling waits in tests
"""
import time
from config.config import Config
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


class WaitUtils:
    """Utility class for waits"""

    @staticmethod
    def wait_for_element(page, selector, timeout=None):
        """Wait for element to be visible"""
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            page.locator(selector).wait_for(timeout=timeout * 1000)
            logger.info(f"Element found: {selector}")
            return True
        except Exception as e:
            logger.error(f"Element not found: {selector} - {str(e)}")
            return False

    @staticmethod
    def wait_for_navigation(page, action_func, timeout=None):
        """Wait for page navigation"""
        timeout = timeout or Config.PAGE_LOAD_TIMEOUT
        try:
            with page.expect_navigation(timeout=timeout * 1000):
                action_func()
            logger.info("Navigation completed")
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}")
            return False

    @staticmethod
    def wait_for_element_clickable(page, selector, timeout=None):
        """Wait for element to be clickable"""
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            locator = page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout * 1000)
            locator.wait_for(state="attached", timeout=timeout * 1000)
            logger.info(f"Element is clickable: {selector}")
            return True
        except Exception as e:
            logger.error(f"Element not clickable: {selector} - {str(e)}")
            return False

    @staticmethod
    def wait_for_text_in_element(page, selector, text, timeout=None):
        """Wait for specific text in element"""
        timeout = timeout or Config.EXPLICIT_WAIT
        try:
            page.locator(selector).wait_for(timeout=timeout * 1000)
            assert text in page.locator(selector).inner_text()
            logger.info(f"Text '{text}' found in {selector}")
            return True
        except Exception as e:
            logger.error(f"Text '{text}' not found in {selector} - {str(e)}")
            return False

    @staticmethod
    def implicit_wait(seconds=None):
        """Wait for specified seconds"""
        seconds = seconds or Config.IMPLICIT_WAIT
        logger.info(f"Waiting for {seconds} seconds...")
        time.sleep(seconds)
