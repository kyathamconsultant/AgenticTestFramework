"""
Example Playwright tests using pytest framework
"""
import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.fixture
def browser():
    """Fixture to provide a browser instance"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Fixture to provide a page instance"""
    page = browser.new_page()
    yield page
    page.close()


def test_page_title(page):
    """Test: Verify page title"""
    page.goto("https://example.com")
    title = page.title()
    assert title == "Example Domain"


def test_page_content(page):
    """Test: Check page content"""
    page.goto("https://example.com")

    # Check if specific text exists
    expect(page).to_have_title("Example Domain")

    # Check for heading
    heading = page.locator("h1")
    expect(heading).to_contain_text("Example Domain")


def test_multiple_navigations(page):
    """Test: Navigate to multiple pages"""
    page.goto("https://example.com")
    assert "example" in page.url

    page.goto("https://example.com")
    assert page.title() == "Example Domain"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
