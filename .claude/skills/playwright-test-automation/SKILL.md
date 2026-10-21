---
name: playwright-test-automation
title: Playwright BDD Automation Standards
description: Industry-standard Playwright automation with Cucumber, Gherkin, and Allure reporting
category: Test Automation
version: 3.1
updated: 2026-07-23
level: Intermediate to Advanced
---

# Playwright BDD Automation Standards

**Comprehensive guide for enterprise-grade test automation with Playwright, Cucumber, and Allure Reporting**

---

## 📋 Table of Contents

1. [Project Structure](#project-structure)
2. [Feature Files & Gherkin](#feature-files--gherkin)
3. [Locator Strategy](#locator-strategy)
4. [Assertions & Validation](#assertions--validation)
5. [Wait Strategy](#wait-strategy)
6. [Test Stability](#test-stability)
7. [Reporting Standards](#reporting-standards)
8. [Step Definitions](#step-definitions)
9. [Configuration](#configuration)
10. [Data Management](#data-management)
11. [Common Pitfalls](#common-pitfalls)

---

## Project Structure

### Feature-Driven Organization

```
project/
├── features/
│   ├── auth/
│   │   ├── login.feature
│   │   ├── logout.feature
│   │   └── password-reset.feature
│   ├── products/
│   │   ├── product-listing.feature
│   │   ├── product-search.feature
│   │   └── product-filters.feature
│   ├── cart/
│   │   ├── add-to-cart.feature
│   │   └── checkout.feature
│   └── orders/
│       ├── order-placement.feature
│       └── order-history.feature
├── steps/
│   ├── auth.steps.ts
│   ├── products.steps.ts
│   ├── cart.steps.ts
│   ├── orders.steps.ts
│   ├── common.steps.ts
│   └── hooks.ts
├── pages/
│   ├── base.page.ts
│   ├── login.page.ts
│   ├── products.page.ts
│   ├── cart.page.ts
│   └── checkout.page.ts
├── test-data/
│   ├── users.json
│   ├── products.json
│   └── test-scenarios.json
├── playwright.config.ts
├── cucumber.js
├── allure-report-config.js
└── package.json
```

---

## Feature Files & Gherkin

### File Naming Convention

| Convention | Format | Example |
|-----------|--------|---------|
| **File Name** | `feature-name.feature` | `login.feature` |
| **Location** | `features/<domain>/` | `features/auth/login.feature` |
| **Case Style** | kebab-case, lowercase | `product-listing.feature` |

### Feature File Structure

**Example: `features/auth/login.feature`**

```gherkin
Feature: User Login to Swag Labs
  As a user
  I want to login to the Swag Labs application
  So that I can access my account and purchase products

  Background:
    Given I navigate to the login page

  @smoke @critical
  Scenario: Successful login with valid credentials
    When I enter email "standard_user@saucedemo.com"
    And I enter password "password123"
    And I click the login button
    Then I should be redirected to the products page
    And I should see the products inventory
    And the page title should be "Swag Labs - Products"

  @critical
  Scenario Outline: Login with different user types
    When I enter email "<email>"
    And I enter password "<password>"
    And I click the login button
    Then I should see the result "<expectedResult>"
    And the page URL should be "<expectedURL>"

    Examples:
      | email                    | password    | expectedResult       | expectedURL        |
      | standard_user@saucedemo  | password123 | success              | /inventory.html    |
      | locked_out_user@saucedemo| password123 | locked_account_error | /auth-v2/login     |
      | problem_user@saucedemo   | password123 | success              | /inventory.html    |

  @negative @regression
  Scenario Outline: Login with invalid credentials
    When I enter email "<email>"
    And I enter password "<password>"
    And I click the login button
    Then I should see error message "<errorMessage>"
    And I should remain on the login page

    Examples:
      | email                   | password      | errorMessage                              |
      | invalid@saucedemo.com   | password123   | Epic sadface: Username and password do not match |
      | standard_user@saucedemo | wrongpassword | Epic sadface: Username and password do not match |
      | ""                      | password123   | Epic sadface: Username is required        |
      | standard_user@saucedemo | ""            | Epic sadface: Password is required        |
```

### Scenario Outline Best Practices

✅ **DO Use Scenario Outlines** for data-driven tests

```gherkin
Scenario Outline: Login with different user types
  When I enter email "<email>"
  And I enter password "<password>"
  And I click the login button
  Then I should see "<expectedResult>"
  
  Examples:
    | email             | password    | expectedResult |
    | user1@test.com    | password123 | success        |
    | user2@test.com    | password123 | success        |
```

❌ **AVOID Repetitive Scenarios**

```gherkin
# Instead of writing same scenario 3 times:
Scenario: Login with user 1 → Use Scenario Outline
Scenario: Login with user 2 → Use Scenario Outline
Scenario: Login with user 3 → Use Scenario Outline
```

---

## Locator Strategy

### Priority-Based Selector Hierarchy

#### **Tier 1: Data Test IDs (MOST STABLE & PREFERRED)**

```typescript
// ✓ BEST - Explicit and stable, won't break on style changes
page.locator('[data-testid="login-button"]')
page.locator('button[data-testid="login-button"]')
```

**Why Use:**
- Decoupled from CSS/HTML structure
- Explicit test automation intent
- Won't break during UI style updates
- Self-documenting

#### **Tier 2: ARIA Roles & Labels (ACCESSIBLE)**

```typescript
// ✓ BEST - Accessible and stable
page.getByRole('button', { name: 'Login' })
page.locator('[aria-label="Close"]')
page.locator('[aria-placeholder="Username"]')
```

**Why Use:**
- Tests actual accessibility
- Ensures screen reader compatibility
- Stable for assistive technology users
- User-centric approach

#### **Tier 3: Semantic HTML (RELIABLE)**

```typescript
// ✓ GOOD - Based on HTML semantics
page.locator('input[name="email"][type="text"]')
page.locator('input[placeholder="Enter email"]')
page.locator('#submit-button')
```

**Why Use:**
- Based on HTML semantics
- Stable structure
- Works without test-specific attributes

#### **Tier 4: CSS & XPath (AVOID)**

```typescript
// ⚠ AVOID - Fragile, breaks with UI changes
page.locator('.btn-primary-lg-v2-hover')  // CSS classes change frequently
page.locator('//button[contains(@class, "btn")]//span[1]')  // Unmaintainable XPath
```

**Why Avoid:**
- Break with CSS refactors
- Hard to read and maintain
- Tightly coupled to UI styling

### Best Practice Examples

```typescript
// ✓ BEST - Combine strategies for robustness
page.locator('[data-testid="submit"] >> role=button')

// ✓ GOOD - Accessibility-first
page.getByRole('textbox', { name: /password/i })

// ✓ GOOD - Chained locators for specificity
page.locator('form[data-testid="login"]').locator('[data-testid="submit"]')

// ⚠ AVOID - Over-specific, brittle
page.locator('div > div > form > div:nth-child(3) > button')
```

---

## Assertions & Validation

### Rule: Always Assert Specifically

❌ **AVOID Generic Assertions**

```typescript
await expect(page).toHaveURL('https://example.com/dashboard')
await expect(loginButton).toBeVisible()
```

✅ **USE Specific Assertions**

```typescript
await expect(page).toHaveURL('https://example.com/dashboard')
await expect(loginButton).toContainText('Login')
await expect(successMessage).toHaveText('Login successful')
```

### Assertion Patterns

#### **After Successful Operations**

```typescript
// ✓ Assert exact success message
await loginPage.login('user@example.com', 'password123')
const successMsg = await page.locator('[data-testid="success-message"]').textContent()
expect(successMsg).toBe('Welcome, John Doe!')

// ✓ Assert navigation occurred
await expect(page).toHaveURL('/dashboard')
await expect(page.locator('h1')).toContainText('Dashboard')
```

#### **After Failed Operations**

```typescript
// ✓ Assert exact error message
await loginPage.login('user@example.com', 'wrongpassword')
const errorMsg = await page.locator('[data-testid="error"]').textContent()
expect(errorMsg).toContain('Invalid credentials')
expect(errorMsg).not.toContain('undefined')
```

#### **Financial & Data-Sensitive Operations**

```typescript
// ✓ Assert exact numeric values
const balance = await page.locator('[data-testid="balance"]').textContent()
expect(balance).toBe('$1,234.56')  // Exact match including formatting

// ✓ Verify account number format
expect(accountNumber).toMatch(/^AC-\d{10}$/)

// ✓ Assert transaction details
expect(transaction.amount).toBe(100.00)
expect(transaction.currency).toBe('USD')
expect(transaction.status).toBe('COMPLETED')
```

### Common Assertion Methods

```typescript
// Text content
expect(text).toBe('Exact match')
expect(text).toContain('substring')
expect(text).toMatch(/regex/)

// Visibility
expect(element).toBeVisible()
expect(element).toBeHidden()
expect(element).not.toBeInViewport()

// State
expect(element).toBeEnabled()
expect(element).toBeDisabled()
expect(element).toBeChecked()
expect(element).toBeFocused()

// Count
expect(rows).toHaveCount(5)
expect(errors).toHaveCount(0)
```

---

## Wait Strategy

### Core Principle: Let Playwright Wait For You

✅ **BEST - Playwright Auto-Waiting**

```typescript
// Auto-waiting handles visibility, actionability, and timing
await page.locator('[data-testid="load"]').click()
await expect(page.locator('[data-testid="result"]')).toBeVisible()
```

❌ **NEVER - Hardcoded Waits**

```typescript
await page.waitForTimeout(2000)  // WRONG - Flaky and slow
await new Promise(resolve => setTimeout(resolve, 1000))  // WRONG
```

### Wait for Dynamic Content

```typescript
// ✓ Wait for dropdown to appear and select
await page.locator('[data-testid="dropdown"]').click()
await page.locator('[data-testid="dropdown-option"]').first().waitFor({ state: 'visible' })
await page.locator('text=Option 1').click()

// ✓ Wait for list to load before counting
await expect(page.locator('[data-testid="item"]')).toHaveCount(10)

// ✓ Wait for input to be ready
await page.locator('input[name="email"]').fill('user@example.com')
```

### Wait for Network Responses

```typescript
// ✓ Wait for API response after action
const responsePromise = page.waitForResponse(
  response => response.url().includes('/api/login') && response.status() === 200
)
await page.locator('[data-testid="login"]').click()
const response = await responsePromise
expect(response.status()).toBe(200)

// ✓ Wait for multiple network requests
await Promise.all([
  page.waitForResponse(r => r.url().includes('/user')),
  page.waitForResponse(r => r.url().includes('/settings')),
  page.locator('[data-testid="refresh"]').click()
])

// ✓ Wait for loading indicator to disappear
await page.locator('[data-testid="spinner"]').waitFor({ state: 'hidden' })
```

### Timeout Configuration

```typescript
// ✓ Standard timeout (30 seconds default)
await expect(element).toBeVisible()

// ✓ Custom timeout for slow operations
await page.waitForURL('https://example.com/dashboard', { timeout: 10000 })

// ✓ Short timeout for immediate responses
await expect(page.locator('[data-testid="error"]')).toBeVisible({ timeout: 3000 })

// ✓ Extended timeout for degraded environments
const perfElement = await page.locator('[data-testid="perf-item"]').waitFor({ timeout: 15000 })
```

---

## Test Stability

### Rule 1: No Test Interdependencies

❌ **BAD - Test depends on previous test**

```typescript
test('User can view profile', () => {
  // Assumes login happened in previous test
  await expect(page.locator('h1')).toContainText('Profile')
})
```

✅ **GOOD - Each test is self-contained**

```typescript
test('User can view profile', async ({ page }) => {
  await loginPage.navigate()
  await loginPage.login('user@example.com', 'password')
  await expect(page).toHaveURL('/profile')
  await expect(page.locator('h1')).toContainText('Profile')
})
```

### Rule 2: Selectors Work Across All States

✅ **GOOD - Selector works with any account**

```typescript
test.beforeEach(async ({ page }) => {
  const users = [
    { email: 'standard@example.com', name: 'Standard User' },
    { email: 'premium@example.com', name: 'Premium User' },
    { email: 'admin@example.com', name: 'Admin User' }
  ]
  // Use data-testid that works for all user types
  await page.locator('[data-testid="user-name"]').waitFor()
})
```

❌ **BAD - Selector assumes specific user**

```typescript
await expect(page.locator('text=John Doe')).toBeVisible()
```

### Rule 3: Use Fixtures for Setup

```typescript
// ✓ Reusable fixture for login
test.beforeEach(async ({ page, context }) => {
  // Setup: Navigate and login fresh for each test
  await page.goto('https://app.example.com')
  await page.locator('[data-testid="email"]').fill('user@example.com')
  await page.locator('[data-testid="password"]').fill('password123')
  await page.locator('[data-testid="login"]').click()
  await expect(page).toHaveURL('/dashboard')
})

test('Should perform action', async ({ page }) => {
  // Test starts with logged-in state
  await page.locator('[data-testid="action-button"]').click()
})
```

### Rule 4: Avoid Global State

❌ **BAD - Shared data affects tests**

```typescript
let testData
test('Setup', () => {
  testData = { id: '123' }
})
test('Use data', () => {
  expect(testData.id).toBe('123')  // Depends on previous test
})
```

✅ **GOOD - Each test has its own data**

```typescript
test('First operation', async () => {
  const id = await createItem()
  expect(id).toBeDefined()
})
test('Second operation', async () => {
  const id = await createItem()  // Fresh data
  expect(id).toBeDefined()
})
```

---

## Reporting Standards

### Screenshot on Failure (Required)

```typescript
// ✓ BEST - Auto-capture on failure
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== 'passed') {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    await page.screenshot({
      path: `test-results/screenshots/${testInfo.title}-${timestamp}.png`,
      fullPage: true
    })
  }
})

// ✓ GOOD - Manual capture at critical points
await page.screenshot({ path: 'test-results/before-submit.png' })
await form.submit()
await page.screenshot({ path: 'test-results/after-submit.png' })
```

### Test Logging for Traceability

```typescript
test('Complex workflow', async ({ page }) => {
  console.log('STEP 1: Navigate to login page')
  await page.goto('https://app.example.com/login')
  
  console.log('STEP 2: Enter credentials')
  await page.locator('[data-testid="email"]').fill('user@example.com')
  await page.locator('[data-testid="password"]').fill('password123')
  
  console.log('STEP 3: Submit form')
  await page.locator('[data-testid="login"]').click()
  
  console.log('STEP 4: Verify redirect')
  await expect(page).toHaveURL('/dashboard')
  
  console.log('TEST PASSED')
})
```

### Video Recording & Tracing

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    video: 'retain-on-failure',  // Record only failed tests
    trace: 'on-first-retry'       // Trace on retry
  }
})

// Optional: Manual video capture
test('Critical checkout flow', async ({ page }) => {
  const video = page.video()
  await video.saveAs('test-results/checkout-video.webm')
})
```

---

## Step Definitions

### Page Object Model Pattern

```typescript
// pages/login.page.ts
import { Page, Locator } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly loginButton: Locator
  readonly errorMessage: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.locator('[data-testid="username"]')
    this.passwordInput = page.locator('[data-testid="password"]')
    this.loginButton = page.locator('[data-testid="login-button"]')
    this.errorMessage = page.locator('[data-testid="error-message"]')
  }

  async goto() {
    await this.page.goto('https://www.saucedemo.com/')
    await this.emailInput.waitFor()
  }

  async fillEmail(email: string) {
    await this.emailInput.fill(email)
  }

  async fillPassword(password: string) {
    await this.passwordInput.fill(password)
  }

  async clickLoginButton() {
    await this.loginButton.click()
  }

  async getErrorMessage(): Promise<string> {
    return await this.errorMessage.textContent() || ''
  }

  async isErrorMessageVisible(): Promise<boolean> {
    return await this.errorMessage.isVisible()
  }
}
```

### Step Implementation with Allure

```typescript
// steps/auth.steps.ts
import { Given, When, Then } from '@cucumber/cucumber'
import { expect, Page } from '@playwright/test'
import * as allure from 'allure-playwright'
import { LoginPage } from '../pages/login.page'

let page: Page
let loginPage: LoginPage

Given('I navigate to the login page', async function() {
  await allure.step('Navigate to login page', async () => {
    loginPage = new LoginPage(page)
    await loginPage.goto()
  })
})

When('I enter email {string}', async function(email: string) {
  await allure.step(`Enter email: ${email}`, async () => {
    await loginPage.fillEmail(email)
  })
})

When('I enter password {string}', async function(password: string) {
  await allure.step(`Enter password: ****`, async () => {
    await loginPage.fillPassword(password)
  })
})

When('I click the login button', async function() {
  await allure.step('Click login button', async () => {
    await loginPage.clickLoginButton()
  })
})

Then('I should be redirected to the products page', async function() {
  await allure.step('Verify redirect to products page', async () => {
    await expect(page).toHaveURL(/.*inventory\.html/)
  })
})

Then('I should see error message {string}', async function(expectedMessage: string) {
  await allure.step(`Verify error message: "${expectedMessage}"`, async () => {
    const errorText = await loginPage.getErrorMessage()
    expect(errorText).toContain(expectedMessage)
  })
})
```

---

## Configuration

### Cucumber Configuration

```javascript
// cucumber.js
module.exports = {
  default: {
    require: ['steps/**/*.ts'],
    requireModule: ['ts-node/register'],
    format: [
      'progress-bar',
      'html:cucumber-report.html',
      'json:test-results/cucumber-report.json'
    ],
    formatOptions: { snippetInterface: 'async-await' },
    parallel: 2,
    retry: 1,
    retryTagFilter: '@flaky',
    strict: true,
    order: 'random'
  }
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "cucumber-js",
    "test:smoke": "cucumber-js --tags '@smoke'",
    "test:critical": "cucumber-js --tags '@critical'",
    "test:regression": "cucumber-js --tags '@regression'",
    "test:parallel": "cucumber-js --parallel 4",
    "allure:report": "allure generate allure-results -o allure-report --clean",
    "allure:open": "allure open allure-report",
    "allure:serve": "allure serve allure-results"
  }
}
```

---

## Data Management

### Externalize Test Data

```json
// test-data/users.json
{
  "validUsers": [
    { "email": "standard_user@saucedemo.com", "password": "password123", "name": "Standard User" },
    { "email": "premium_user@saucedemo.com", "password": "password123", "name": "Premium User" }
  ],
  "invalidUsers": [
    { "email": "locked_out_user@saucedemo.com", "password": "password123", "error": "locked out" },
    { "email": "invalid@example.com", "password": "wrongpass", "error": "invalid credentials" }
  ]
}
```

### Environment Variables

```bash
# .env.example (commit to repo)
TEST_USER_EMAIL=standard_user@saucedemo.com
TEST_USER_PASSWORD=***redacted***
APP_URL=https://www.saucedemo.com

# .env (local only, don't commit)
TEST_USER_EMAIL=standard_user@saucedemo.com
TEST_USER_PASSWORD=password123
APP_URL=https://www.saucedemo.com
```

---

## Common Pitfalls

| Problem | ❌ Bad Practice | ✓ Solution |
|---------|-----------------|-----------|
| **Element not found** | Generic locators | Use data-testid attributes |
| **Flaky waits** | `await page.waitForTimeout(2000)` | Use auto-waiting & explicit waits |
| **Hardcoded credentials** | Username/password in features | Move to test-data JSON files |
| **Brittle selectors** | CSS class selectors `.btn-v2` | Use data-testid or ARIA roles |
| **Test interdependencies** | Scenario depends on previous | Use Background/Given setup |
| **No traceability** | Missing Allure labels | Add severity, owner, feature labels |
| **Flaky scenarios** | No retry logic | Use @flaky tag + retryTagFilter |
| **Hard to debug** | No video recordings | Enable video capture on failure |
| **Unclear validations** | Generic assertions | Assert exact values |
| **Missing parameters** | Hardcoded test data | Document expected vs actual |

---

## Quick Reference

### Testing Commands

```bash
# Run tests
npm run test                    # All tests
npm run test:smoke            # Smoke tests (@smoke)
npm run test:critical         # Critical tests (@critical)
npm run test:regression       # Regression tests (@regression)
npm run test:parallel         # Parallel execution (4 workers)

# Allure reports
npm run allure:report         # Generate report
npm run allure:open           # View in browser
npm run allure:serve          # Live server (auto-refresh)
```

### Gherkin Syntax

```gherkin
Feature: Feature description          # What users can do
  Scenario: Single test case          # One test case
  Scenario Outline: Data-driven test  # Multiple examples
    Examples: | data |                # Test data rows
  
  Given <precondition>                # Setup state
  When <action>                        # User action
  Then <assertion>                     # Verify result
  And <additional step>                # Additional step
```

### Tags

```gherkin
@smoke            # Smoke tests
@critical         # Must pass
@regression       # Full suite
@flaky            # Retry enabled
@wip              # Work in progress
@skip             # Skip test
```

---

**Version:** BDD Standard v3.1  
**Framework:** Playwright + Cucumber + Allure  
**Last Updated:** 2026-07-23  
**Expertise Level:** Intermediate to Advanced
