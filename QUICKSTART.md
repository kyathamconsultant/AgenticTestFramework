# Quick Start Guide - SauceDemo Test Automation

Get up and running with the framework in 5 minutes!

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
playwright install
```

### Step 2: Verify Installation (1 minute)

```bash
behave --dry-run
```

Expected output: List of features and scenarios without execution

### Step 3: Run Your First Test (1 minute)

```bash
behave features/login.feature
```

### Step 4: View Results (1 minute)

```bash
allure serve results/allure-results
```

## 🎯 Your First Test Run

### Run Specific Test Scenario

```bash
behave features/login.feature -n "Successful login with valid credentials"
```

### Watch It Run

- Browser opens automatically (Chrome by default)
- Performs login actions
- Displays results in terminal

## 📊 Understanding Results

### Terminal Output

```
Feature: Login Functionality
  Scenario: Successful login with valid credentials
    Given I navigate to the login page     ✓
    When I enter username "standard_user"  ✓
    And I enter password "secret_sauce"    ✓
    And I click the login button           ✓
    Then I should be redirected to the products page ✓

1 feature passed, 0 failed
```

### Allure Report

```
allure serve results/allure-results
```

Opens browser showing:
- Test summary
- Pass/fail statistics
- Execution timeline
- Screenshots of failures
- Detailed logs

## 🔍 Common Commands

### Run All Tests

```bash
behave
```

### Run Specific Feature

```bash
behave features/cart.feature
```

### Run with Tags

```bash
behave -t @smoke
```

### Run in Headless Mode (Faster)

```bash
set HEADLESS=true
behave
```

### Verbose Output

```bash
behave -v
```

### Stop on First Failure

```bash
behave -x
```

## 🛠️ Quick Configuration

### Edit .env file to change:

```env
# Browser (chromium, firefox, webkit)
BROWSER=chromium

# Run headless (faster, no GUI)
HEADLESS=false

# Base URL
BASE_URL=https://www.saucedemo.com/

# Test credentials
TEST_USER_STANDARD=standard_user
TEST_PASSWORD=secret_sauce
```

## 📁 File Locations

- **Tests**: `features/`
- **Step Code**: `features/steps/`
- **Page Objects**: `pages/`
- **Configuration**: `.env`, `config/config.py`
- **Test Data**: `test_data/`
- **Results**: `results/`
- **Screenshots**: `results/screenshots/`
- **Logs**: `results/logs/`

## 🎨 Project Structure at a Glance

```
features/           ← Test scenarios (Gherkin)
├── login.feature
├── products.feature
├── cart.feature
├── checkout.feature
└── steps/          ← Step implementations
    ├── login_steps.py
    ├── product_steps.py
    ├── cart_steps.py
    └── checkout_steps.py

pages/              ← Page Object Model
├── base_page.py    ← Base class
├── login_page.py
├── products_page.py
├── cart_page.py
├── checkout_page.py
└── order_confirmation_page.py

config/             ← Configuration
├── config.py
└── .env

utilities/          ← Helper utilities
├── logger_utils.py
├── wait_utils.py
├── screenshot_utils.py
└── data_reader.py

test_data/          ← Test data files
├── login_data.csv
├── product_data.json
└── checkout_data.json

results/            ← Test results
├── allure-results/
├── screenshots/
└── logs/
```

## 🚀 Next Steps

### 1. Explore Test Scenarios

Open and read:
- `features/login.feature` - Understand test format
- `features/products.feature` - See more scenarios

### 2. Review Page Objects

Check out:
- `pages/base_page.py` - Common methods
- `pages/login_page.py` - Login page methods

### 3. Add Your Own Test

Create a new scenario in `features/login.feature`:

```gherkin
Scenario: My first test
  Given I navigate to the login page
  When I enter username "standard_user"
  And I enter password "secret_sauce"
  And I click the login button
  Then I should be redirected to the products page
```

Then run:
```bash
behave features/login.feature -n "My first test"
```

### 4. Check Logs and Screenshots

```bash
# View latest logs
type results/logs/login_steps.py.log

# View screenshots
dir results/screenshots/
```

## 💡 Pro Tips

### Tip 1: Run Tests Faster

```bash
# Headless mode (no GUI)
set HEADLESS=true
behave
```

### Tip 2: Debug a Failing Test

```bash
# See all output
behave -v features/login.feature

# Stop on first failure
behave -x features/login.feature

# Check screenshots
dir results/screenshots/
```

### Tip 3: Focus on Specific Tests

```bash
# Run single scenario
behave features/login.feature -n "Successful login"

# Run by tag
behave -t @critical
```

### Tip 4: Generate Beautiful Reports

```bash
# Create Allure report
allure serve results/allure-results

# Browser opens automatically with visualized data
```

### Tip 5: Understand Test Data

```python
# CSV data
results/test_data/login_data.csv

# JSON data
results/test_data/product_data.json

# Add your own data and reference in tests
```

## ❓ FAQ

### Q: Tests are running too fast, I can't see them
**A**: Set `SLOW_MO=500` in .env to add 500ms delay between actions

### Q: Browser doesn't open
**A**: Set `HEADLESS=false` in .env

### Q: Tests are slow
**A**: Set `HEADLESS=true` in .env

### Q: Can't see screenshots
**A**: Check `results/screenshots/` folder

### Q: Where are the test logs?
**A**: Check `results/logs/` folder (one log per module)

### Q: How do I add new tests?
**A**: Create feature file → Add step definitions → Add page objects

### Q: How do I run tests in Firefox?
**A**: Set `BROWSER=firefox` in .env

### Q: Can I run tests on multiple browsers?
**A**: Currently one at a time, change BROWSER in .env

## ✅ Verify Everything Works

```bash
# 1. Install
pip install -r requirements.txt

# 2. Verify installation
behave --dry-run

# 3. Run one test
behave features/login.feature -n "Successful login with valid credentials"

# 4. Check results
allure serve results/allure-results

# ✅ All working!
```

## 📚 Learn More

- **Feature Format**: Read a .feature file in `features/`
- **Step Definitions**: Check `features/steps/` Python files
- **Page Objects**: Review `pages/` folder
- **Full Documentation**: See README.md

## 🎓 Learning Resources

1. **Behave**: https://behave.readthedocs.io/
2. **Playwright**: https://playwright.dev/python/
3. **Allure**: https://docs.qameta.io/allure/
4. **Gherkin**: https://cucumber.io/docs/gherkin/

---

**Happy Testing! 🚀**

Need help? Check the full README.md or CLAUDE.md for detailed information.
