---
name: playwright-test-automation
description: Implementation standards for this Python Behave + Playwright (sync API) + Allure framework - locator strategy, Page Object Model classes, step definitions, assertions with expect(), wait strategy, hooks in environment.py, test data, configuration, logging and Allure attachments. Use when writing, generating, fixing, or refactoring page objects, step definitions, hooks, or utilities, or when choosing selectors from a live DOM.
license: Proprietary - internal QA team use
compatibility: Python 3.8+, playwright>=1.40 (sync API), behave>=1.2.6, allure-behave. Not for TypeScript @playwright/test projects.
metadata:
  author: QA Team
  version: "4.0"
  updated: "2026-10-30"
  category: test-automation
  supersedes: "3.1 (TypeScript/Cucumber-JS edition)"
---

# Playwright Python Implementation Standards

How to implement tests in this framework. Related skills:
- **Feature files** (Gherkin wording, tags, structure): the `cucumber-feature-file` skill.
- **What to test** (risk): the `application-domain` skill.
- **Reviewing the result:** the `test-code-review` skill.

## Contents
1. [Project layout](#1-project-layout)
2. [Locator strategy](#2-locator-strategy)
3. [Page objects](#3-page-objects)
4. [Step definitions](#4-step-definitions)
5. [Assertions](#5-assertions)
6. [Waits](#6-waits)
7. [Hooks & browser lifecycle](#7-hooks--browser-lifecycle)
8. [Test data & configuration](#8-test-data--configuration)
9. [Logging & reporting](#9-logging--reporting)
10. [Commands](#10-commands)
11. [Common pitfalls](#11-common-pitfalls)

## 1. Project layout

| Layer | Path | Naming | Rule |
|-------|------|--------|------|
| Feature files | `features/<feature>.feature` | kebab-case | Follow the `cucumber-feature-file` skill |
| Step definitions | `features/steps/<feature_snake>_steps.py` | snake_case | Thin: call page objects, then assert |
| Page objects | `pages/<page_snake>_page.py` → `class <Page>Page(BasePage)` | snake_case / PascalCase | Selectors and UI interaction only |
| Test data | `test_data/<feature_snake>_data.json` / `.csv` | snake_case | Read via `utilities/data_reader.py` |
| Config | `config/config.py` (`Config`) + `.env` | UPPER_SNAKE | Every setting has a safe default |
| Utilities | `utilities/` | snake_case | Logging, waits, screenshots, data |
| Hooks | `environment.py` | – | Browser lifecycle, screenshots, Allure |

**Never generate** `.spec.ts`, `playwright.config.ts`, `package.json` test scripts or `tests/` folders. This is not a TypeScript project.

## 2. Locator strategy

**Selectors must come from the live DOM.** Use the MCP `browser_snapshot` / `browser_generate_locator` tools. Never guess. Choose the highest available tier:

| Tier | Strategy | Python example | When |
|------|----------|----------------|------|
| 1 | Test id (`data-test` on SauceDemo) | `page.get_by_test_id("login-button")` or `"[data-test='login-button']"` | Always, when present |
| 2 | Role + accessible name | `page.get_by_role("button", name="Login")` | No test id |
| 3 | Label / placeholder / stable id or name | `page.get_by_placeholder("Username")`, `"#user-name"` | No role or name |
| 4 | CSS class / XPath | `".inventory_item"` | Last resort; justify in a comment |

- SauceDemo uses `data-test`, not Playwright's default `data-testid`. Call `context.playwright.selectors.set_test_id_attribute("data-test")` once, before creating pages, if you use `get_by_test_id`.
- Scope repeated elements through their container, not by index: `page.locator(".inventory_item").filter(has_text=name).get_by_role("button")`.
- ❌ Avoid: `nth-child` chains, absolute XPath, auto-generated or styling classes, and text that changes with locale or content.
- Store selector strings as **class constants**. Build parameterised locators in methods.

## 3. Page objects

```python
"""Page object for the SauceDemo cart page."""
from typing import List

from playwright.sync_api import Page, Locator

from pages.base_page import BasePage
from utilities.logger_utils import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    """Cart page: list, remove and check out items."""

    CART_ITEM = "[data-test='inventory-item']"
    ITEM_NAME = "[data-test='inventory-item-name']"
    CHECKOUT_BUTTON = "[data-test='checkout']"

    def __init__(self, page: Page):
        super().__init__(page)

    def item(self, name: str) -> Locator:
        return self.page.locator(self.CART_ITEM).filter(has_text=name)

    def item_names(self) -> List[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def remove(self, name: str) -> None:
        logger.info(f"Removing '{name}' from cart")
        self.item(name).get_by_role("button", name="Remove").click()

    def checkout(self) -> None:
        self.page.locator(self.CHECKOUT_BUTTON).click()
```

| Rule | Detail |
|------|--------|
| Inherit `BasePage` | Reuse its helpers. Don't re-implement navigation or screenshots |
| Intent-level methods | `login(username, password)`, `add_to_cart(name)`, not `click_button_3()` |
| Return state, don't assert | `item_names()`, `error_text()`, `is_loaded()`. Steps do the asserting |
| Let errors propagate | Don't wrap Playwright calls in `try/except Exception: return False`. That discards the timeout and selector details. If you must add context: `raise AssertionError(f"Cart item '{name}' not found") from e` |
| Never log secrets | Log the selector or field name, not the value typed into password fields |
| One page or component per class | Shared widgets (header, cart badge) can be their own component class |
| Type hints | On all public methods |

## 4. Step definitions

```python
"""Step definitions for cart.feature."""
from behave import given, when, then
from playwright.sync_api import expect

from pages.cart_page import CartPage


@when('I remove "{product}" from my cart')
def step_remove_from_cart(context, product):
    context.cart_page = CartPage(context.browser)
    context.cart_page.remove(product)


@then("my cart contains {count:d} item(s)")
def step_cart_count(context, count):
    names = context.cart_page.item_names()
    assert len(names) == count, f"Cart count: expected {count}, got {len(names)} {names}"
```

| Rule | Detail |
|------|--------|
| Thin steps | No selectors and no raw `page.click` in steps. Go through page objects |
| Reuse before writing | Run `behave --steps-catalog` first. Behave registers steps globally, so a duplicate pattern raises `AmbiguousStep` |
| Typed parameters | `{count:d}`, `{price:f}` instead of `int(count)` |
| Wording matches the feature | Step text follows the `cucumber-feature-file` skill (declarative, first person) |
| `context` attributes | Set in Given/When, read in Then. Name them clearly (`context.cart_page`). Nothing survives between scenarios except what hooks create |
| Credentials | Resolve by role from `Config` (`Config.TEST_USER_STANDARD`, `Config.TEST_PASSWORD`). Never from literals in steps |

## 5. Assertions

Prefer Playwright's **web-first assertions**. They retry until the timeout, which removes most flakiness:

```python
from playwright.sync_api import expect
import re

expect(page.get_by_test_id("error")).to_have_text(re.compile("Username is required"))
expect(page).to_have_url(re.compile(r"/inventory\.html$"))
expect(page.locator("[data-test='inventory-item']")).to_have_count(6)
expect(page.get_by_test_id("shopping-cart-badge")).to_be_hidden()
```

- Assert the **outcome the user sees**, specifically: exact text, count, URL or value. Never `assert page.click_x()`, which only proves no exception was raised.
- Plain `assert` with a message for computed values: `assert total == expected, f"Total: expected {expected}, got {total}"`.
- **Money:** compare with `decimal.Decimal`, never floats, and assert subtotal, tax and total separately (see the financial risks in the `application-domain` skill).
- Sorting: assert the whole list against `sorted(...)`, not just the first item.

## 6. Waits

| ✅ Do | ❌ Don't |
|------|---------|
| Rely on locator auto-waiting (`click`, `fill`) and `expect(...)` | `time.sleep(n)` / `page.wait_for_timeout(n)` |
| `locator.wait_for(state="visible")` for explicit state | Polling loops with sleeps |
| `page.wait_for_url(...)`, `page.wait_for_load_state("networkidle")` only when needed | Raising timeouts globally to hide slowness |
| `page.expect_response("**/api/cart")` around the triggering action | Waiting on arbitrary DOM after a network call |

Timeouts come from `Config.EXPLICIT_WAIT` (seconds × 1000 for Playwright). Set them once with `page.set_default_timeout(...)` in the hook, not per call.

## 7. Hooks & browser lifecycle

`environment.py` owns the browser. Standards:
- **Fresh isolated state per scenario:** create a new `browser.new_context(...)` and `new_page()` per scenario (a cookie-free session). Launch the browser once per run in `before_all` for speed.
- **Clean up in `after_scenario` in every case**, including when setup failed (`getattr(context, "page", None)` guards).
- **On failure:** take a screenshot, attach it to Allure, and optionally save a trace (`context.tracing.start(screenshots=True, snapshots=True)` in `before_scenario`, then `stop(path=...)` on failure).
- Read browser, headless mode, slow-mo and viewport only from `Config`. CI sets `HEADLESS=true`.

## 8. Test data & configuration

- Inline Gherkin examples carry **illustrative** data. Bulk, generated or sensitive-looking data goes in `test_data/` and is read through `utilities/data_reader.py`.
- Credentials and URLs come from env vars via `Config`. Never hard-code them in pages, steps or data files.
- New settings: add them to `Config` with a default, to `.env.example`, and to the configuration table in `CLAUDE.md`.

## 9. Logging & reporting

- `logger = get_logger(__name__)` in every module. `info` for actions, `debug` for detail, `error` only for real failures. No `print`.
- Allure attachments: `allure.attach(page.screenshot(), name="cart", attachment_type=allure.attachment_type.PNG)`.
- Run with the Allure formatter: `behave -f allure_behave.formatter:AllureFormatter -o results/allure-results`. The CI runner script already does this.
- Tag scenarios for reporting and CI selection using the tag vocabulary in the `cucumber-feature-file` skill.

## 10. Commands

```bash
behave --dry-run                                  # parse + step binding check
behave --steps-catalog                            # list existing steps before writing new ones
behave features/cart.feature                      # run one feature
behave features/cart.feature -n "Remove item"     # run one scenario by name
behave --tags "@smoke and not @wip"               # by tag expression
HEADLESS=true bash .claude/skills/cicd-pipeline/scripts/run_tests.sh   # CI-identical run
allure serve results/allure-results               # view report
```

## 11. Common pitfalls

| Problem | ❌ Bad practice | ✅ Solution |
|---------|----------------|-------------|
| Element not found / brittle | CSS classes, `nth-child`, XPath | Tier 1–2 locators from the live DOM |
| Flaky timing | `time.sleep`, `wait_for_timeout` | Auto-wait + `expect(...)` |
| Errors hidden | `except Exception: return False` | Let it raise, or re-raise with context |
| False-green tests | `assert page.click_login()` | Assert the visible outcome |
| Secrets leak | Typed values logged; credentials in steps | Mask logs; credentials from `Config` |
| Test interdependence | Scenario relies on a previous one | New context per scenario; setup in Given |
| Ambiguous steps | Same pattern in two step files | `--steps-catalog`, reuse or reword |
| Money mismatches | Float arithmetic | `Decimal`, assert each component |
| Wrong stack | `.spec.ts`, `npx playwright test` | Python page objects + Behave steps |
