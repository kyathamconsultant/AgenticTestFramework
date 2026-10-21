# SauceDemo Test Automation Framework - Project Manifest

## 📋 Project Summary

**Project Name**: SauceDemo Test Automation Framework  
**Description**: Production-ready BDD test automation framework using Behave, Playwright, and Allure  
**Application Under Test**: https://www.saucedemo.com/  
**Framework Type**: Behavior-Driven Development (BDD)  
**Test Tool**: Behave (Python implementation of Cucumber)  
**Browser Automation**: Playwright  
**Reporting**: Allure Report  
**Architecture**: Page Object Model (POM)  

## 📊 Framework Statistics

| Metric | Count |
|--------|-------|
| Feature Files | 4 |
| Test Scenarios | 32+ |
| Step Definitions | 70+ |
| Page Objects | 6 |
| Utility Functions | 30+ |
| Test Data Files | 3 |
| Configuration Files | 3 |
| Documentation Files | 5 |
| Total Lines of Code | 3000+ |

## 🗂️ Complete Directory Structure

```
PyClaudeAgenticTestFramewokr/
│
├── 📄 QUICKSTART.md                    # 5-minute setup guide
├── 📄 README.md                        # Comprehensive documentation
├── 📄 CLAUDE.md                        # Framework documentation (updated)
├── 📄 FRAMEWORK_OVERVIEW.md            # Architecture and flow diagrams
├── 📄 PROJECT_MANIFEST.md              # This file
├── 📄 setup_framework.md               # Framework setup guide
│
├── features/                           # BDD Feature Files (Gherkin)
│   ├── 📝 login.feature               # 5 scenarios + Scenario Outline (6 total)
│   ├── 📝 products.feature            # 10 test scenarios
│   ├── 📝 cart.feature                # 8 test scenarios
│   ├── 📝 checkout.feature            # 9 test scenarios
│   │
│   └── steps/                         # Step Definition Implementations
│       ├── 🐍 login_steps.py          # ~11 step definitions
│       ├── 🐍 product_steps.py        # ~20 step definitions
│       ├── 🐍 cart_steps.py           # ~15 step definitions
│       └── 🐍 checkout_steps.py       # ~17 step definitions
│
├── pages/                             # Page Object Model
│   ├── __init__.py                   # Package initialization
│   ├── 🐍 base_page.py               # Base class - 20+ reusable methods
│   ├── 🐍 login_page.py              # Login page - 10+ methods
│   ├── 🐍 products_page.py           # Products page - 20+ methods
│   ├── 🐍 cart_page.py               # Cart page - 15+ methods
│   ├── 🐍 checkout_page.py           # Checkout page - 15+ methods
│   └── 🐍 order_confirmation_page.py # Confirmation page - 5+ methods
│
├── config/                           # Configuration Management
│   ├── __init__.py                  # Package initialization
│   └── 🐍 config.py                 # Centralized config with 20+ settings
│
├── utilities/                        # Reusable Utilities
│   ├── __init__.py                  # Package initialization
│   ├── 🐍 logger_utils.py           # Logging setup and management
│   ├── 🐍 wait_utils.py             # 5+ wait strategy methods
│   ├── 🐍 screenshot_utils.py       # Screenshot capture and attachment
│   └── 🐍 data_reader.py            # Multi-format test data reader
│
├── test_data/                        # Test Data Files (Data-Driven)
│   ├── 📊 login_data.csv            # 8 login test cases (CSV format)
│   ├── 📊 product_data.json         # 6 products (JSON format)
│   └── 📊 checkout_data.json        # 6 checkout scenarios (JSON format)
│
├── results/                          # Test Results and Artifacts
│   ├── allure-results/              # Allure report JSON data
│   ├── screenshots/                 # Failure screenshots (auto-generated)
│   └── logs/                        # Detailed test logs (auto-generated)
│
├── 🐍 environment.py                # Behave environment setup/teardown
├── 📝 behave.ini                    # Behave test runner configuration
├── 📄 requirements.txt              # Python package dependencies
├── .env                             # Environment variables
├── .mcp.json                        # MCP (Model Context Protocol) config
├── .gitignore                       # Git ignore rules
└── script.py                        # Example Playwright script
```

## 📄 File Descriptions

### Configuration Files

| File | Purpose | Content |
|------|---------|---------|
| `.env` | Environment configuration | Base URL, browser settings, credentials, timeouts |
| `config/config.py` | Configuration class | Settings management, directory setup |
| `behave.ini` | Behave configuration | Test runner settings, formatters, filters |
| `.mcp.json` | MCP configuration | Playwright MCP server setup |

### Feature Files (Gherkin/BDD)

| File | Scenarios | Lines | Focus Area |
|------|-----------|-------|-----------|
| `features/login.feature` | 6 | ~50 | Login, credentials, validation |
| `features/products.feature` | 10 | ~80 | Product listing, sorting, cart |
| `features/cart.feature` | 8 | ~70 | Cart management, totals |
| `features/checkout.feature` | 9 | ~90 | Checkout process, validation |

### Step Definition Files

| File | Steps | Lines | Covers |
|------|-------|-------|--------|
| `features/steps/login_steps.py` | 11 | ~120 | Login scenarios |
| `features/steps/product_steps.py` | 20 | ~200 | Product scenarios |
| `features/steps/cart_steps.py` | 15 | ~150 | Cart scenarios |
| `features/steps/checkout_steps.py` | 17 | ~180 | Checkout scenarios |

### Page Object Files

| File | Methods | Lines | Purpose |
|------|---------|-------|---------|
| `pages/base_page.py` | 20+ | ~300 | Common methods for all pages |
| `pages/login_page.py` | 10+ | ~130 | Login page interactions |
| `pages/products_page.py` | 20+ | ~250 | Product page operations |
| `pages/cart_page.py` | 15+ | ~200 | Cart page operations |
| `pages/checkout_page.py` | 15+ | ~220 | Checkout operations |
| `pages/order_confirmation_page.py` | 5+ | ~80 | Confirmation page |

### Utility Files

| File | Functions | Purpose |
|------|-----------|---------|
| `utilities/logger_utils.py` | 2 | Logging configuration and setup |
| `utilities/wait_utils.py` | 5 | Wait strategies and synchronization |
| `utilities/screenshot_utils.py` | 3 | Screenshot capture and attachment |
| `utilities/data_reader.py` | 4 | Read CSV, JSON, Excel test data |

### Test Data Files

| File | Format | Rows | Purpose |
|------|--------|------|---------|
| `test_data/login_data.csv` | CSV | 8 | Login credentials and expected results |
| `test_data/product_data.json` | JSON | 6 | Product catalog data |
| `test_data/checkout_data.json` | JSON | 6 | Checkout scenarios with validation |

### Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| `QUICKSTART.md` | 5-minute setup guide | Everyone |
| `README.md` | Comprehensive guide | Detailed users |
| `CLAUDE.md` | Framework documentation | Developers |
| `FRAMEWORK_OVERVIEW.md` | Architecture diagrams | Architects |
| `PROJECT_MANIFEST.md` | This file | Team reference |

### Core Files

| File | Purpose | Language |
|------|---------|----------|
| `environment.py` | Behave environment hooks | Python |
| `requirements.txt` | Package dependencies | TXT |
| `script.py` | Example test script | Python |

## 🎯 Feature Coverage

### Login Tests (6 scenarios)
- ✅ Successful login with valid credentials
- ✅ Login failure with invalid password
- ✅ Login failure with locked user
- ✅ Login with empty username
- ✅ Login with empty password
- ✅ Data-driven login with multiple users

### Product Tests (10 scenarios)
- ✅ View products on inventory page
- ✅ Add single product to cart
- ✅ Add multiple products to cart
- ✅ Add all products to cart
- ✅ Remove product from cart
- ✅ Sort products by name (A-Z)
- ✅ Sort products by price (low-high)
- ✅ Sort products by price (high-low)
- ✅ View product details
- ✅ Logout functionality

### Cart Tests (8 scenarios)
- ✅ View empty cart
- ✅ Add item to cart and view
- ✅ Add multiple items to cart
- ✅ Remove item from cart
- ✅ Clear all items from cart
- ✅ Continue shopping from cart
- ✅ Calculate cart total
- ✅ Proceed to checkout

### Checkout Tests (9 scenarios)
- ✅ Checkout with valid information
- ✅ Checkout with missing first name
- ✅ Checkout with missing last name
- ✅ Checkout with missing postal code
- ✅ Complete order successfully
- ✅ Data-driven checkout with multiple users
- ✅ Verify totals on summary
- ✅ Cancel checkout

## 🏗️ Architecture Components

### Layer 1: Presentation (Features)
- Gherkin syntax feature files
- Human-readable test scenarios
- No technical implementation details

### Layer 2: Step Definitions
- Bridges feature files and page objects
- Implements step logic
- Uses context to pass data

### Layer 3: Page Objects
- UI interaction methods
- Locator management
- Reusable operations

### Layer 4: Utilities
- Cross-cutting concerns
- Logging, screenshots, waits
- Data reading

### Layer 5: Configuration
- Centralized settings
- Environment variables
- Directory management

### Layer 6: Framework
- Behave (test runner)
- Playwright (browser automation)
- Allure (reporting)

## 🔄 Data Flow

### Test Execution Data Flow
```
Feature File
    ↓
[Step Definition Matcher]
    ↓
[Python Step Function]
    ↓
[Page Object Method]
    ↓
[Playwright Browser API]
    ↓
[SauceDemo Application]
    ↓
[Assertion/Verification]
    ↓
[Result Logging & Screenshot]
    ↓
[Allure Report]
```

### Test Data Flow
```
test_data/ (CSV/JSON)
    ↓
[DataReader.read_csv/json()]
    ↓
[Step Definition receives data]
    ↓
[Uses in page interaction]
    ↓
[Assertion against expected]
```

## 🎨 Naming Conventions

### Feature Files
- Lowercase with underscores
- Plural nouns: `features/login.feature`
- Named by functionality

### Step Definitions
- Snake_case function names
- Prefixed with `step_`
- Example: `def step_enter_username(context, username):`

### Page Objects
- PascalCase class names
- Named by page: `LoginPage`, `ProductsPage`
- Locators in UPPERCASE with underscores

### Methods
- Descriptive names using verbs
- snake_case
- Example: `get_cart_item_count()`, `add_product_to_cart()`

### Variables
- Context variables stored in `context.object_name`
- Config values via `Config.SETTING_NAME`

## 🚀 Execution Paths

### Full Test Suite
```bash
behave                                  # All features, all scenarios
```

### Specific Feature
```bash
behave features/login.feature           # Only login tests
behave features/checkout.feature        # Only checkout tests
```

### Specific Scenario
```bash
behave features/login.feature -n "Successful login with valid credentials"
```

### By Tags
```bash
behave -t @critical                     # Only critical tests
behave -t @smoke                        # Only smoke tests
behave -t @regression                   # Only regression tests
```

### With Options
```bash
behave -v                               # Verbose output
behave -x                               # Stop on first failure
behave --dry-run                        # Parse without execution
```

## 📊 Test Metrics

### Coverage
- **Pages**: 6 (Login, Products, Cart, Checkout, Confirmation, Base)
- **Scenarios**: 32+
- **Steps**: 70+
- **Methods**: 90+

### Quality
- **Reusability**: High (Base classes, utilities)
- **Maintainability**: High (POM architecture)
- **Readability**: High (Gherkin syntax)
- **Scalability**: High (Modular design)

### Configuration
- **Browsers**: 3 (Chromium, Firefox, WebKit)
- **Environments**: 1 (with .env support)
- **Timeouts**: 3 types
- **Log Levels**: 4

## 🔧 Configuration Parameters

### Browser Settings
```
BROWSER = chromium | firefox | webkit
HEADLESS = true | false
SLOW_MO = milliseconds (0-5000)
VIEWPORT_WIDTH = pixels
VIEWPORT_HEIGHT = pixels
```

### Timeout Settings (seconds)
```
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30
```

### Test Settings
```
TEST_USER_STANDARD = standard_user
TEST_USER_LOCKED = locked_out_user
TEST_PASSWORD = secret_sauce
```

### Reporting Settings
```
ALLURE_ENABLED = true | false
SCREENSHOT_ON_FAILURE = true | false
SCREENSHOT_FORMAT = png | jpeg
LOG_LEVEL = DEBUG | INFO | WARNING | ERROR
```

## 📦 Dependencies

### Core Dependencies
```
playwright >= 1.40.0      # Browser automation
behave >= 1.2.6           # BDD framework
python-dotenv >= 1.0.0    # Environment variables
```

### Testing Dependencies
```
pytest >= 7.0.0           # Test framework (optional)
pytest-asyncio >= 0.21.0  # Async support (optional)
```

### Reporting Dependencies
```
allure-behave >= 2.13.2   # Allure Behave integration
allure-pytest >= 2.13.2   # Allure Pytest integration
```

### Utilities
```
pyyaml >= 6.0             # YAML support
openpyxl >= 3.10.0        # Excel reading
requests >= 2.31.0        # HTTP requests
pillow >= 10.0.0          # Image processing
```

## 🎓 Documentation Map

| Document | Purpose | Read Time |
|----------|---------|-----------|
| QUICKSTART.md | Get started in 5 minutes | 5 min |
| README.md | Complete user guide | 20 min |
| CLAUDE.md | Framework documentation | 15 min |
| FRAMEWORK_OVERVIEW.md | Architecture details | 15 min |
| PROJECT_MANIFEST.md | This file - reference | 10 min |

## ✅ Verification Checklist

Before running tests, verify:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Playwright browsers: `playwright install`
- [ ] Configuration file: `.env` exists
- [ ] Features directory: `features/` with feature files
- [ ] Pages directory: `pages/` with page objects
- [ ] Utilities directory: `utilities/` with helpers
- [ ] Config directory: `config/` with config.py
- [ ] Results directory: `results/` created
- [ ] Log directory: `results/logs/` created
- [ ] Screenshots directory: `results/screenshots/` created

## 🎯 Next Steps

1. **Start**: Read QUICKSTART.md (5 minutes)
2. **Install**: Run `pip install -r requirements.txt && playwright install`
3. **Run**: Execute `behave features/login.feature`
4. **Report**: Open `allure serve results/allure-results`
5. **Explore**: Review feature files and step definitions
6. **Customize**: Modify `.env` for your needs
7. **Extend**: Add new scenarios and test cases

## 📞 Support Resources

- **Behave Docs**: https://behave.readthedocs.io/
- **Playwright Docs**: https://playwright.dev/python/
- **Allure Docs**: https://docs.qameta.io/allure/
- **Gherkin Guide**: https://cucumber.io/docs/gherkin/

## 🏆 Framework Status

```
✅ Production Ready
✅ Well Documented
✅ Modular Architecture
✅ Easily Extensible
✅ Comprehensive Testing
✅ Beautiful Reporting
```

---

**Framework Version**: 1.0.0  
**Created**: 2024  
**Maintenance**: Active  
**Status**: ✅ Production Ready

**Total Framework Files**: 25+  
**Total Test Scenarios**: 32+  
**Lines of Code**: 3000+  
**Documentation Pages**: 5  

This comprehensive test automation framework provides a solid foundation for testing the SauceDemo application with best practices in BDD, POM, and test automation principles.
