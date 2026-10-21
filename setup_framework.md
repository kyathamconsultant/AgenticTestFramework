# SauceDemo Test Automation Framework - Setup Guide

## Project Structure

```
PyClaudeAgenticTestFramewokr/
├── features/                           # Behave feature files (Gherkin)
│   ├── login.feature
│   ├── products.feature
│   ├── cart.feature
│   ├── checkout.feature
│   └── steps/
│       ├── login_steps.py
│       ├── product_steps.py
│       ├── cart_steps.py
│       └── checkout_steps.py
│
├── pages/                              # Page Object Model
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── order_confirmation_page.py
│
├── config/                             # Configuration files
│   ├── __init__.py
│   ├── config.py
│   ├── browser_config.py
│   └── .env
│
├── test_data/                          # Test data (CSV, Excel, JSON)
│   ├── login_data.csv
│   ├── product_data.json
│   └── checkout_data.xlsx
│
├── utilities/                          # Helper utilities
│   ├── __init__.py
│   ├── screenshot_utils.py
│   ├── report_utils.py
│   ├── data_reader.py
│   ├── wait_utils.py
│   └── logger_utils.py
│
├── results/                            # Test results
│   ├── allure-results/
│   ├── screenshots/
│   └── logs/
│
├── behave.ini                          # Behave configuration
├── conftest.py                         # pytest configuration
├── environment.py                      # Environment setup for behave
├── requirements.txt                    # Python dependencies
├── CLAUDE.md                          # Project documentation
├── .env                               # Environment variables
└── README.md                          # Framework documentation
```

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browsers:
   ```bash
   playwright install
   ```

3. Run tests:
   ```bash
   behave
   ```

4. Generate Allure report:
   ```bash
   allure serve results/allure-results
   ```

## Framework Features

- ✅ BDD with Behave (Gherkin syntax)
- ✅ Page Object Model architecture
- ✅ Data-driven testing
- ✅ Screenshot capture on failures
- ✅ Allure Report integration
- ✅ Comprehensive logging
- ✅ Configurable browsers
- ✅ Reusable components
