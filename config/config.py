"""
Configuration management for the test framework
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    FEATURES_DIR = PROJECT_ROOT / "features"
    PAGES_DIR = PROJECT_ROOT / "pages"
    TEST_DATA_DIR = PROJECT_ROOT / "test_data"
    RESULTS_DIR = PROJECT_ROOT / "results"
    SCREENSHOTS_DIR = RESULTS_DIR / "screenshots"
    LOGS_DIR = RESULTS_DIR / "logs"
    ALLURE_RESULTS_DIR = RESULTS_DIR / "allure-results"

    # Application URL
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")

    # Browser settings
    BROWSER_TYPE = os.getenv("BROWSER", "chromium").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))
    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

    # Timeouts (in seconds)
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Test data
    TEST_USER_STANDARD = os.getenv("TEST_USER_STANDARD", "standard_user")
    TEST_USER_LOCKED = os.getenv("TEST_USER_LOCKED", "locked_out_user")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "secret_sauce")

    # Allure configuration
    ALLURE_ENABLED = os.getenv("ALLURE_ENABLED", "true").lower() == "true"
    ALLURE_RESULTS_PATH = str(ALLURE_RESULTS_DIR)

    # Screenshot settings
    TAKE_SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOT_FORMAT = os.getenv("SCREENSHOT_FORMAT", "png")  # png or jpeg

    @staticmethod
    def ensure_directories():
        """Create required directories if they don't exist"""
        for directory in [Config.SCREENSHOTS_DIR, Config.LOGS_DIR, Config.ALLURE_RESULTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)


# Ensure directories are created
Config.ensure_directories()
