# SauceDemo Test Automation Framework

**Status**: Production Ready ✅  
**Version**: 1.0.0  
**Python**: 3.8+  
**Last Updated**: 2024

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Architecture](#architecture)
- [Test Coverage](#test-coverage)
- [Reporting](#reporting)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Resources](#resources)

---

## Overview

A **production-ready BDD test automation framework** for the SauceDemo e-commerce application, demonstrating industry best practices:

- ✅ **Behavior-Driven Development** (BDD) with Gherkin syntax for stakeholder collaboration
- ✅ **Page Object Model** (POM) architecture for maintainability and reusability
- ✅ **Data-Driven Testing** with CSV, JSON, and Excel support
- ✅ **Cross-Browser Testing** (Chromium, Firefox, WebKit)
- ✅ **Comprehensive Reporting** with Allure Report and automatic screenshots
- ✅ **Robust Logging** with multi-level logging to console and files
- ✅ **Smart Wait Strategies** with explicit waits and configurable timeouts

---

## Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- Git (optional, for version control)

### Installation & Setup

```bash
# 1. Clone or navigate to the project
cd PyClaudeAgenticTestFramewokr

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install

# 5. Configure environment
cp .env.example .env  # if available, or create .env
```

### Run Your First Test

```bash
# Run login tests
behave features/login.feature

# Run all tests
behave

# View Allure report
allure serve results/allure-results
```

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Test Framework | Behave (BDD/Gherkin) | Latest |
| Browser Automation | Playwright | Latest |
| Reporting | Allure Report | Latest |
| Logging | Python logging | Built-in |
| Data Formats | CSV, JSON, Excel | Native support |
| Architecture | Page Object Model | Custom implementation |

---

## Project Structure

```
PyClaudeAgenticTestFramewokr/
├── features/                    # BDD feature files (Gherkin)
│   ├── login.feature           # Login scenarios (5 main + 1 outline)
│   ├── products.feature        # Product catalog (10 scenarios)
│   ├── cart.feature            # Shopping cart (8 scenarios)
│   ├── checkout.feature        # Checkout flow (9 scenarios)
│   └── steps/                  # Step implementations
│       ├── login_steps.py      # Login step definitions (~11)
│       ├── product_steps.py    # Product steps (~20)
│       ├── cart_steps.py       # Cart steps (~15)
│       └── checkout_steps.py   # Checkout steps (~17)
│
├── pages/                       # Page Object Model
│   ├── base_page.py            # Base class (20+ reusable methods)
│   ├── login_page.py           # Login page interactions
│   ├── products_page.py        # Product catalog interactions
│   ├── cart_page.py            # Cart interactions
│   ├── checkout_page.py        # Checkout interactions
│   └── order_confirmation_page.py # Confirmation page
│
├── config/
│   ├── config.py               # Centralized configuration manager
│   └── .env                    # Environment variables (not in git)
│
├── utilities/
│   ├── logger_utils.py         # Centralized logging setup
│   ├── wait_utils.py           # Smart wait strategies
│   ├── screenshot_utils.py     # Screenshot capture & management
│   └── data_reader.py          # CSV/JSON/Excel data reading
│
├── test_data/
│   ├── login_data.csv          # Login test cases (8 scenarios)
│   ├── product_data.json       # Product catalog (6 products)
│   └── checkout_data.json      # Checkout scenarios (6 cases)
│
├── results/                     # Test artifacts (auto-generated)
│   ├── allure-results/         # Allure report data
│   ├── screenshots/            # Failure screenshots
│   └── logs/                   # Test execution logs
│
├── environment.py              # Behave hooks & environment setup
├── behave.ini                  # Behave configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── .gitignore                  # Git ignore patterns
├── CLAUDE.md                   # This file (project docs)
└── README.md                   # User guide
```

---

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd PyClaudeAgenticTestFramewokr
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 4. Create Environment File

```bash
# Copy template and update values
cp .env.template .env

# Or create manually with these variables:
# BASE_URL, BROWSER, HEADLESS, IMPLICIT_WAIT, EXPLICIT_WAIT, etc.
```

### 5. Verify Installation

```bash
# Check Playwright browsers are installed
playwright install-deps

# Run a quick test
behave features/login.feature --dry-run
```

---

## Configuration

### Environment Variables (.env)

```env
# Application Configuration
BASE_URL=https://www.saucedemo.com/
APP_NAME=SauceDemo

# Browser Configuration
BROWSER=chromium                 # Options: chromium, firefox, webkit
HEADLESS=false                   # Run in headless mode: true/false
SLOW_MO=0                        # Slow down actions in milliseconds
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# Timeouts (seconds)
IMPLICIT_WAIT=10                 # Default wait for elements
EXPLICIT_WAIT=15                 # Explicit wait timeout
PAGE_LOAD_TIMEOUT=30             # Page load timeout

# Logging Configuration
LOG_LEVEL=INFO                   # Options: DEBUG, INFO, WARNING, ERROR
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Test Credentials
TEST_USER_STANDARD=standard_user
TEST_USER_LOCKED=locked_out_user
TEST_PASSWORD=secret_sauce

# Reporting
ALLURE_ENABLED=true
SCREENSHOT_ON_FAILURE=true
SCREENSHOT_FORMAT=png
REPORT_PATH=results/allure-results
```

### Dynamic Configuration

Edit `config/config.py` for programmatic configuration management:

```python
from config.config import Config

config = Config()
base_url = config.get('BASE_URL')
browser = config.get('BROWSER', default='chromium')
wait_time = config.get_int('EXPLICIT_WAIT')
```

---

## Running Tests

### Basic Execution

```bash
# Run all tests
behave

# Run specific feature
behave features/login.feature

# Run specific scenario
behave features/login.feature -n "Successful login"

# Run with specific tags
behave -t @smoke
behave -t @regression
behave -t @sanity
```

### Advanced Options

```bash
# Verbose output with step details
behave -v

# Very verbose with logging
behave -vv

# Dry run (parse only, no execution)
behave --dry-run

# Stop on first failure
behave -x

# Parallel execution (if configured)
behave --parallel

# Output in different formats
behave -f json -o results/behave.json
behave -f html -o results/behave.html
```

### Generating Reports

```bash
# Serve Allure report (opens in browser)
allure serve results/allure-results

# Generate static HTML report
allure generate results/allure-results -o allure-report --clean

# Open generated report
allure open allure-report
```

---

## Architecture

### Page Object Model (POM)

**Benefits:**
- **Maintainability**: UI changes only require updates in page objects
- **Readability**: Tests are self-documenting
- **Reusability**: Page methods used across multiple tests
- **Scalability**: Easy to add new pages and tests

**Implementation:**

```python
# Base class with common methods
class BasePage:
    def __init__(self, page):
        self.page = page
    
    def navigate_to(self, url):
        self.page.goto(url)
    
    def click_element(self, selector):
        self.page.click(selector)
    
    def fill_input(self, selector, text):
        self.page.fill(selector, text)
    
    def wait_for_element(self, selector, timeout=None):
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def take_screenshot(self, name):
        self.page.screenshot(path=f"results/screenshots/{name}.png")

# Specific page implementation
class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    
    def login(self, username, password):
        self.fill_input(self.USERNAME_INPUT, username)
        self.fill_input(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
```

### Wait Strategy

- ✅ **Explicit waits** using Playwright's `wait_for_*` methods
- ✅ **Configurable timeouts** via environment variables
- ✅ **No hardcoded sleeps** for stability
- ✅ **Proper error handling** with meaningful error messages

```python
# Good: Explicit wait
page.wait_for_selector("#element", timeout=15000)

# Bad: Hardcoded sleep
time.sleep(5)
```

### Logging Strategy

- **Console output** for immediate feedback
- **File logs** in `results/logs/{module}.log`
- **Log levels**: DEBUG, INFO, WARNING, ERROR
- **Contextual logging** with step names and test data

```python
from utilities.logger_utils import get_logger

logger = get_logger(__name__)
logger.info(f"Logging in as {username}")
logger.error(f"Element not found: {selector}")
```

---

## Test Coverage

### Login Tests (5 scenarios + 1 data-driven)
- ✅ Successful login with valid credentials
- ✅ Invalid password handling
- ✅ Locked user account (login fails)
- ✅ Empty username validation
- ✅ Empty password validation
- ✅ Multiple user data-driven tests

**File**: `features/login.feature`

### Product Tests (10 scenarios)
- ✅ View products inventory
- ✅ Add single product to cart
- ✅ Add multiple products
- ✅ Add all products
- ✅ Remove product from cart
- ✅ Sort by name (A-Z)
- ✅ Sort by price (low-high)
- ✅ Sort by price (high-low)
- ✅ View product details
- ✅ Logout functionality

**File**: `features/products.feature`

### Cart Tests (8 scenarios)
- ✅ View empty cart
- ✅ Add item to cart
- ✅ Add multiple items
- ✅ Remove specific item
- ✅ Clear entire cart
- ✅ Continue shopping
- ✅ Calculate totals (verify amounts)
- ✅ Proceed to checkout

**File**: `features/cart.feature`

### Checkout Tests (9 scenarios)
- ✅ Checkout with valid information
- ✅ Missing first name validation
- ✅ Missing last name validation
- ✅ Missing postal code validation
- ✅ Complete order successfully
- ✅ Multiple user data-driven checkout
- ✅ Verify order totals
- ✅ Cancel checkout
- ✅ Payment confirmation

**File**: `features/checkout.feature`

**Total**: 32+ test scenarios covering critical user paths

---

## Reporting

### Allure Report Features

#### 1. Overview Dashboard
- Pass/Fail ratio visualization
- Test execution statistics
- Timeline of execution
- Quick health check

#### 2. Test Results
- Individual scenario details
- Execution time per test
- Status (Pass/Fail/Skip)
- Steps with timing

#### 3. Failures Analysis
- Failed scenario details
- Automatic failure screenshots
- Error messages and logs
- Stack traces when applicable

#### 4. Timeline View
- Test execution order
- Duration per test
- Resource usage
- Chronological sequence

#### 5. Trends Analysis
- Historical data over time
- Pass rate trends
- Flaky test detection
- Performance metrics

### Generating Reports

```bash
# Generate and serve Allure report
allure serve results/allure-results

# Generate static HTML (no server required)
allure generate results/allure-results -o allure-report --clean

# View specific test details
allure open allure-report
```

---

## Development Workflow

### Adding New Tests

```
1. Create Feature File
   └─ features/new_feature.feature (write Gherkin scenarios)

2. Implement Step Definitions
   └─ features/steps/new_feature_steps.py (implement Given/When/Then)

3. Create Page Objects
   └─ pages/new_page.py (if new page needed)

4. Add Test Data
   └─ test_data/new_data.csv|json (external test data)

5. Run Tests
   └─ behave features/new_feature.feature

6. Review Results
   └─ allure serve results/allure-results
```

### Step Definition Pattern

```python
@given('I navigate to the login page')
def step_navigate_to_login(context):
    login_page = LoginPage(context.browser)
    login_page.navigate_to_login()
    assert login_page.is_login_page_displayed()
    context.login_page = login_page

@when('I enter valid credentials')
def step_enter_credentials(context):
    context.login_page.login(
        username=context.config.get('TEST_USER_STANDARD'),
        password=context.config.get('TEST_PASSWORD')
    )

@then('I should be logged in successfully')
def step_verify_login(context):
    assert context.login_page.is_dashboard_displayed()
```

### Updating Selectors

When UI changes:

```python
# Update in page object only
class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"  # Update here
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"

# Step definitions remain unchanged
```

### Best Practices

1. **Single Responsibility**: Each step does one thing
2. **DRY Principle**: Reuse page object methods
3. **Clear Naming**: Use descriptive variable/method names
4. **Error Handling**: Handle edge cases gracefully
5. **Data-Driven**: Externalize test data
6. **Logging**: Log important actions
7. **Screenshots**: Capture on failures automatically
8. **Configuration**: Use environment variables

---

## Troubleshooting

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **Element not found** | Selector changed or wrong | Check selector in page object; update if needed |
| **Timeout errors** | Element takes too long to load | Increase `EXPLICIT_WAIT` in `.env` or use conditional waits |
| **Screenshot not captured** | Wrong path or permissions | Verify `results/screenshots/` directory exists |
| **Allure report missing** | Results directory empty | Run tests first with `behave`, then `allure serve` |
| **Browser not found** | Playwright browsers not installed | Run `playwright install` |
| **Module not found** | Virtual environment not activated | Activate venv: `source venv/Scripts/activate` |
| **Login always fails** | Wrong credentials or API change | Check test credentials in `.env` against live app |
| **Flaky tests** | Timing issues or unstable selectors | Use explicit waits instead of sleeps |

### Debugging

```bash
# Run with detailed logging
LOG_LEVEL=DEBUG behave features/login.feature -v

# Dry run to check syntax
behave --dry-run

# Run single scenario
behave features/login.feature -n "Successful login" -v

# Check current browser configuration
python -c "from config.config import Config; print(Config().get('BROWSER'))"
```

### Logs Location

```
results/
├── logs/
│   ├── login_steps.log
│   ├── products_page.log
│   └── checkout_steps.log
├── screenshots/
│   └── failed_scenario_timestamp.png
└── allure-results/
    └── (Allure JSON files)
```

---

## Contributing

### Guidelines

1. **Feature Branch**: Create branch for new tests
   ```bash
   git checkout -b feature/add-payment-tests
   ```

2. **Write Tests**: Follow Gherkin syntax and POM pattern

3. **Test Locally**: Run all tests before pushing
   ```bash
   behave --dry-run
   behave
   allure serve results/allure-results
   ```

4. **Update Documentation**: Keep feature files and steps documented

5. **Code Review**: Request review before merging

6. **CI/CD Integration**: Ensure tests pass in pipeline

### Code Style

- **Python**: Follow PEP 8
- **Naming**: Use snake_case for functions/variables
- **Selectors**: Store as class constants
- **Comments**: Only for non-obvious logic
- **Line Length**: Max 100 characters

---

## CI/CD Integration

### Jenkins/GitLab CI Pipeline

```bash
#!/bin/bash

# Install dependencies
pip install -r requirements.txt
playwright install

# Run tests with JSON output for Allure
behave -f json -o results/allure-results/behave.json

# Generate Allure report
allure generate results/allure-results -o allure-report --clean

# Archive results
tar -czf test-results.tar.gz results/

# Exit with test status
exit $?
```

### GitHub Actions Example

```yaml
name: Test Automation
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: playwright install
      - run: behave -f json -o results/allure-results/behave.json
      - uses: actions/upload-artifact@v2
        with:
          name: allure-results
          path: results/
```

---

## Performance Optimization

- ✅ **Parallel Execution**: Use `behave --parallel` (if configured)
- ✅ **Headless Mode**: Set `HEADLESS=true` for faster runs
- ✅ **Timeout Tuning**: Adjust `EXPLICIT_WAIT` based on app responsiveness
- ✅ **Resource Cleanup**: Proper browser/context closure
- ✅ **Selective Tagging**: Run only relevant tests with `@tag`

---

## Resources

### Official Documentation
- [Behave Documentation](https://behave.readthedocs.io/)
- [Playwright Python API](https://playwright.dev/python/)
- [Allure Report](https://docs.qameta.io/allure/)
- [Gherkin Language Guide](https://cucumber.io/docs/gherkin/)

### Recommended Reading
- Page Object Model Pattern
- BDD Best Practices
- Test Data Management
- Selenium/Playwright Locator Strategies

### Community
- Behave Issues: https://github.com/behave/behave/issues
- Playwright Issues: https://github.com/microsoft/playwright/issues
- Stack Overflow: Tag `behave`, `playwright`, `bdd`

---

## License

Specify your license here (e.g., MIT, Apache 2.0)

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review existing GitHub issues
3. Contact team lead or create new issue

---

**Last Updated**: October 2026  
**Maintained By**: QA Team  
**Framework Status**: Production Ready ✅
