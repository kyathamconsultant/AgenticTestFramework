"""
Screenshot utility for capturing screenshots during tests
"""
import os
from datetime import datetime
from pathlib import Path
from config.config import Config
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


class ScreenshotUtils:
    """Utility class for screenshots"""

    @staticmethod
    def take_screenshot(page, name=None, scenario_name=None):
        """Take a screenshot of the current page"""
        try:
            if not Config.SCREENSHOTS_DIR.exists():
                Config.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if scenario_name:
                filename = f"{scenario_name}_{name}_{timestamp}.{Config.SCREENSHOT_FORMAT}"
            else:
                filename = f"{name or 'screenshot'}_{timestamp}.{Config.SCREENSHOT_FORMAT}"

            screenshot_path = Config.SCREENSHOTS_DIR / filename

            page.screenshot(path=str(screenshot_path), full_page=True)
            logger.info(f"Screenshot taken: {screenshot_path}")

            return str(screenshot_path)
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return None

    @staticmethod
    def take_screenshot_on_failure(page, scenario_name):
        """Take screenshot when test fails"""
        if Config.TAKE_SCREENSHOT_ON_FAILURE:
            return ScreenshotUtils.take_screenshot(
                page,
                name="failure",
                scenario_name=scenario_name
            )
        return None

    @staticmethod
    def attach_screenshot_to_allure(screenshot_path):
        """Attach screenshot to Allure report"""
        try:
            import allure
            if screenshot_path and Path(screenshot_path).exists():
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=Path(screenshot_path).name,
                        attachment_type=allure.attachment_type.PNG
                    )
                logger.info(f"Screenshot attached to Allure: {screenshot_path}")
        except ImportError:
            logger.warning("Allure not available for screenshot attachment")
        except Exception as e:
            logger.error(f"Failed to attach screenshot to Allure: {str(e)}")
