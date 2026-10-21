"""
Base Page Object Model class
All page objects will inherit from this class
"""
from config.config import Config
from utilities.logger_utils import get_logger
from utilities.wait_utils import WaitUtils
from utilities.screenshot_utils import ScreenshotUtils

logger = get_logger(__name__)


class BasePage:
    """Base class for all page objects"""

    def __init__(self, page):
        """Initialize base page"""
        self.page = page
        self.wait_utils = WaitUtils
        self.screenshot_utils = ScreenshotUtils
        self.base_url = Config.BASE_URL
        logger.info(f"Initialized {self.__class__.__name__}")

    def navigate_to(self, url=None):
        """Navigate to URL"""
        target_url = url or self.base_url
        logger.info(f"Navigating to: {target_url}")
        self.page.goto(target_url, wait_until="networkidle")

    def get_page_title(self):
        """Get page title"""
        title = self.page.title()
        logger.info(f"Page title: {title}")
        return title

    def get_page_url(self):
        """Get current page URL"""
        url = self.page.url
        logger.info(f"Current URL: {url}")
        return url

    def click_element(self, selector):
        """Click an element"""
        try:
            logger.info(f"Clicking element: {selector}")
            self.page.click(selector)
            return True
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {str(e)}")
            return False

    def fill_input(self, selector, value):
        """Fill input field"""
        try:
            logger.info(f"Filling input {selector} with value: {value}")
            self.page.fill(selector, value)
            return True
        except Exception as e:
            logger.error(f"Failed to fill input {selector}: {str(e)}")
            return False

    def get_text(self, selector):
        """Get text from element"""
        try:
            text = self.page.inner_text(selector)
            logger.info(f"Got text from {selector}: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from {selector}: {str(e)}")
            return None

    def get_attribute(self, selector, attribute):
        """Get attribute value"""
        try:
            value = self.page.get_attribute(selector, attribute)
            logger.info(f"Got attribute {attribute} from {selector}: {value}")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute {attribute} from {selector}: {str(e)}")
            return None

    def is_element_visible(self, selector, timeout=None):
        """Check if element is visible"""
        try:
            timeout = timeout or Config.EXPLICIT_WAIT
            self.page.locator(selector).wait_for(state="visible", timeout=timeout * 1000)
            logger.info(f"Element is visible: {selector}")
            return True
        except Exception as e:
            logger.error(f"Element not visible: {selector} - {str(e)}")
            return False

    def is_element_enabled(self, selector):
        """Check if element is enabled"""
        try:
            is_disabled = self.page.locator(selector).is_disabled()
            result = not is_disabled
            logger.info(f"Element {selector} enabled: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to check if element is enabled {selector}: {str(e)}")
            return False

    def select_dropdown_option(self, selector, option_text):
        """Select option from dropdown by text"""
        try:
            logger.info(f"Selecting option '{option_text}' from dropdown {selector}")
            self.page.select_option(selector, option_text)
            return True
        except Exception as e:
            logger.error(f"Failed to select option '{option_text}' from {selector}: {str(e)}")
            return False

    def scroll_to_element(self, selector):
        """Scroll to element"""
        try:
            logger.info(f"Scrolling to element: {selector}")
            self.page.locator(selector).scroll_into_view_if_needed()
            return True
        except Exception as e:
            logger.error(f"Failed to scroll to element {selector}: {str(e)}")
            return False

    def wait_for_element(self, selector, timeout=None):
        """Wait for element to appear"""
        timeout = timeout or Config.EXPLICIT_WAIT
        return self.wait_utils.wait_for_element(self.page, selector, timeout)

    def take_screenshot(self, name="screenshot"):
        """Take screenshot of current page"""
        return self.screenshot_utils.take_screenshot(self.page, name)

    def take_screenshot_on_failure(self, scenario_name):
        """Take screenshot on test failure"""
        return self.screenshot_utils.take_screenshot_on_failure(self.page, scenario_name)

    def execute_script(self, script, arg=None):
        """Execute JavaScript"""
        try:
            logger.info(f"Executing script: {script}")
            if arg:
                result = self.page.evaluate(script, arg)
            else:
                result = self.page.evaluate(script)
            logger.info(f"Script result: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to execute script: {str(e)}")
            return None

    def switch_to_frame(self, selector):
        """Switch to iframe"""
        try:
            logger.info(f"Switching to frame: {selector}")
            frame = self.page.frame_locator(selector)
            return frame
        except Exception as e:
            logger.error(f"Failed to switch to frame {selector}: {str(e)}")
            return None

    def get_all_elements_count(self, selector):
        """Get count of elements matching selector"""
        try:
            count = self.page.locator(selector).count()
            logger.info(f"Found {count} elements matching selector: {selector}")
            return count
        except Exception as e:
            logger.error(f"Failed to count elements {selector}: {str(e)}")
            return 0
