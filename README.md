# SauceDemo Test Automation Framework

A comprehensive BDD (Behavior-Driven Development) test automation framework for the SauceDemo e-commerce application using Python, Behave (Gherkin), Page Object Model (POM), and Allure Reporting.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Data](#test-data)
- [Reporting](#reporting)
- [Best Practices](#best-practices)

## ✨ Features

- **BDD Framework**: Behave with Gherkin syntax for readable test scenarios
- **Page Object Model**: Well-organized, maintainable page object classes
- **Data-Driven Testing**: Support for CSV, JSON, and Excel test data
- **Screenshot Capture**: Automatic screenshots on test failures
- **Allure Reporting**: Comprehensive test reports with visualizations
- **Cross-Browser Support**: Chrome, Firefox, and WebKit
- **Configurable**: Easy to configure via .env file
- **Logging**: Detailed logging for debugging and monitoring
- **Reusable Components**: Base classes and utilities for rapid test development

## 📁 Project Structure

```
PyClaudeAgenticTestFramewokr/
├── features/                           # BDD Feature files (Gherkin)
│   ├── login.feature                  # Login scenarios
│   ├── products.feature               # Product listing scenarios
│   ├── cart.feature                   # Shopping cart scenarios
│   ├── checkout.feature               # Checkout scenarios
│   └── steps/                         # Step definitions
│       ├── login_steps.py             # Login step implementations
│       ├── product_steps.py           # Product step implementations
│       ├── cart_steps.py              # Cart step implementations
│       └── checkout_steps.py          # Checkout step implementations
│
├── pages/                              # Page Object Model
│   ├── base_page.py                   # Base class for all pages
│   ├── login_page.py                  # Login page object
│   ├── products_page.py               # Products page object
│   ├── cart_page.py                   # Cart page object
│   ├── checkout_page.py               # Checkout page object
│   └── order_confirmation_page.py     # Order confirmation page object
│
├── config/                             # Configuration management
│   ├── config.py                      # Main configuration class
│   └── .env                           # Environment variables
│
├── test_data/                          # Test data files
│   ├── login_data.csv                 # Login test data
│   ├── product_data.json              # Product data
│   └── checkout_data.json             # Checkout test data
│
├── utilities/                          # Helper utilities
│   ├── logger_utils.py                # Logging utilities
│   ├── wait_utils.py                  # Wait and synchronization utilities
│   ├── screenshot_utils.py            # Screenshot capture utilities
│   └── data_reader.py                 # Test data reader
│
├── results/                            # Test results and artifacts
│   ├── allure-results/                # Allure report data
│   ├── screenshots/                   # Screenshots on failure
│   └── logs/                          # Detailed test logs
│
├── environment.py                      # Behave environment setup
├── behave.ini                         # Behave configuration
├── requirements.txt                   # Python dependencies
├── .env                               # Environment variables
├── CLAUDE.md                          # Project documentation
└── README.md                          # This file
```

## 🔧 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Playwright installed
- Node.js (optional, for MCP support)

## 📦 Installation

### 1. Clone or Navigate to Project

```bash
cd PyClaudeAgenticTestFramewokr
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

```bash
playwright install
```

### 4. Verify Installation

```bash
behave --dry-run
```

## ⚙️ Configuration

### Environment Variables (.env file)

```env
# Application
BASE_URL=https://www.saucedemo.com/

# Browser
BROWSER=chromium          # chromium, firefox, webkit
HEADLESS=false            # true or false
SLOW_MO=0                 # milliseconds for slowdown
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# Timeouts (seconds)
IMPLICIT_WAIT=10
EXPLICIT_WAIT=15
PAGE_LOAD_TIMEOUT=30

# Logging
LOG_LEVEL=INFO            # DEBUG, INFO, WARNING, ERROR

# Test Credentials
TEST_USER_STANDARD=standard_user
TEST_USER_LOCKED=locked_out_user
TEST_PASSWORD=secret_sauce

# Allure
ALLURE_ENABLED=true

# Screenshots
SCREENSHOT_ON_FAILURE=true
SCREENSHOT_FORMAT=png     # png or jpeg
```

## 🧪 Running Tests

### Run All Tests

```bash
behave
```

### Run Specific Feature File

```bash
behave features/login.feature
```

### Run Specific Scenario

```bash
behave features/login.feature -n "Successful login with valid credentials"
```

### Run with Specific Tags

```bash
behave -t @smoke
behave -t @regression
```

### Run in Headless Mode

```bash
# Modify .env file or set environment variable
set HEADLESS=true
behave
```

### Run with Parallel Execution (if enabled)

```bash
behave --parallel
```

### Verbose Output

```bash
behave -v
```

## 📊 Test Data

### CSV Format (login_data.csv)

```csv
username,password,expected_result,error_message
standard_user,secret_sauce,success,
invalid_user,wrong_password,failure,Username and password do not match
```

### JSON Format (product_data.json)

```json
[
  {
    "id": 1,
    "name": "Sauce Labs Backpack",
    "price": 29.99
  }
]
```

### Reading Test Data in Steps

```python
from utilities.data_reader import DataReader

# Read CSV
login_data = DataReader.read_csv("login_data.csv")

# Read JSON
product_data = DataReader.read_json("product_data.json")

# Auto-detect format
any_data = DataReader.get_test_data("filename.csv")
```

## 📈 Reporting

### Generate Allure Report

```bash
# After tests run, generate report
allure serve results/allure-results
```

This opens an interactive HTML report in your browser showing:
- Test summary and statistics
- Failed tests with screenshots
- Timeline view
- Test behaviors and history
- Trends and analytics

### Report Features

- ✅ Pass/Fail summary
- 📸 Screenshots on failures
- 📝 Detailed logs
- ⏱️ Execution time
- 🏷️ Test tags and categories

## 📝 Writing Test Cases

### Feature File Example

```gherkin
Feature: Login Functionality
  As a user
  I want to login
  So that I can access products

  Background:
    Given I navigate to the login page

  Scenario: Successful login
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be redirected to the products page
```

### Step Definition Example

```python
@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username"""
    login_page = context.login_page
    login_page.enter_username(username)

@then('I should be redirected to the products page')
def step_verify_products_page(context):
    """Verify products page"""
    products_page = ProductsPage(context.browser)
    assert products_page.is_products_page_displayed()
```

## 🎯 Best Practices

1. **Maintain Page Objects**: Keep page objects focused on single pages
2. **DRY Principle**: Reuse methods and utilities
3. **Meaningful Names**: Use clear, descriptive test names
4. **Data-Driven**: Use external test data files
5. **Logging**: Log important actions and assertions
6. **Screenshots**: Take screenshots for visual verification
7. **Wait Strategies**: Use explicit waits instead of hard sleeps
8. **Error Handling**: Provide meaningful error messages
9. **Test Organization**: Group related tests with tags
10. **Documentation**: Keep features and steps well-documented

## 🏷️ Test Tags

Use tags to organize and filter tests:

```gherkin
@smoke
@critical
Scenario: Critical user flow
```

Run specific tag:
```bash
behave -t @smoke
```

## 🔍 Debugging

### Enable Detailed Logging

```env
LOG_LEVEL=DEBUG
```

### View Logs

Logs are saved in `results/logs/` directory

### Debug Specific Scenario

```bash
behave features/login.feature -n "Scenario name" --no-capture
```

## 🐛 Troubleshooting

### Tests not finding elements

- Check selector in Page Object
- Take screenshot for visual inspection
- Verify application has loaded
- Check browser console for errors

### Playwright connection issues

```bash
# Reinstall browsers
playwright install

# Clear cache
rm -rf ~/.cache/ms-playwright/
```

### Allure report not generating

```bash
# Ensure results directory exists
mkdir -p results/allure-results

# Check file permissions
```

## 📚 Additional Resources

- [Behave Documentation](https://behave.readthedocs.io/)
- [Playwright Python Guide](https://playwright.dev/python/)
- [Allure Report Documentation](https://docs.qameta.io/allure/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/)

## 🤝 Contributing

To add new test cases:

1. Create feature file in `features/`
2. Create step definitions in `features/steps/`
3. Add page objects to `pages/` if needed
4. Add test data to `test_data/`
5. Run and verify tests

## 📄 License

This framework is provided as-is for testing the SauceDemo application.

## ✉️ Support

For issues or questions:
1. Check the logs in `results/logs/`
2. Review screenshots in `results/screenshots/`
3. Check Allure report for detailed test information

---

**Framework Version**: 1.0.0  
**Last Updated**: 2024  
**Maintained By**: Test Automation Team
