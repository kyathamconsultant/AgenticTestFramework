---
name: cucumber-feature-file
description: Write, review, or refactor Cucumber/Gherkin .feature files to industry standards - declarative business language, Given/When/Then semantics, Background, Rule, Scenario Outline with Examples, data tables, tagging taxonomy, naming, and formatting. Use when asked to create, add, review, clean up, or convert test cases into feature files or BDD scenarios, for this Behave (Python) framework or any Cucumber-family tool.
license: Proprietary - internal QA team use
compatibility: Gherkin 6+ syntax. Verified against Behave 1.3.x (supports Rule and named Examples). Step-catalog and dry-run commands are Behave-specific.
metadata:
  author: QA Team
  version: "1.0"
  updated: "2026-10-30"
  category: bdd-test-design
---

# Cucumber Feature File Standards

Feature files are **living documentation**. A product owner should be able to read them without knowing the UI or the code. The automation must still be able to run every line.

## Workflow

When creating or changing a feature file:

1. **Understand the behaviour.** Collect the business rules, acceptance criteria and the risks to cover. Use the `application-domain` skill for e-commerce risk analysis.
2. **Reuse existing steps first.** Run `behave --steps-catalog` (or read `features/steps/*.py`) and phrase new steps to match existing ones wherever the meaning is the same.
3. **Write the feature** following the [Structure](#structure) and [Writing rules](#writing-rules) below.
4. **Dry-run it:** `behave --dry-run features/<file>.feature`. Fix syntax errors. List any undefined steps.
5. **Implement the missing steps** with page objects (see the `playwright-test-automation` skill), then run the feature for real.
6. **Self-review** against the [Review checklist](#review-checklist) before handing it over.

## File conventions

| Item | Standard | Example |
|------|----------|---------|
| Location | `features/` (group into `features/<domain>/` once there are more than ~10 files) | `features/checkout.feature` |
| File name | lowercase kebab-case, named after the capability, not a page or a ticket | `order-checkout.feature`, not `page3.feature` or `JIRA-123.feature` |
| One feature per file | One `Feature:` per file, one business capability per feature | |
| Encoding & indent | UTF-8, **2 spaces** per level, no tabs, no trailing whitespace | |
| Spacing | One blank line between scenarios; none inside a scenario | |
| Size | 3–7 steps per scenario; up to ~10–15 scenarios per feature (split by `Rule:` or file beyond that) | |

## Structure

```gherkin
@checkout
Feature: Order checkout
  As a shopper with items in my cart
  I want to provide my details and confirm my order
  So that I receive the products I selected

  Background:
    Given I am logged in as a "standard" user
    And my cart contains "Sauce Labs Backpack" and "Sauce Labs Bike Light"

  Rule: Customer details are mandatory

    @negative @regression
    Scenario Outline: Checkout is blocked when a required detail is missing
      When I submit checkout details without a <field>
      Then checkout is blocked with the error "<error>"

      Examples: Missing details
        | field       | error                   |
        | first name  | First Name is required  |
        | last name   | Last Name is required   |
        | postal code | Postal Code is required |

  Rule: A completed order is confirmed to the customer

    @smoke @critical
    Scenario: Customer completes an order with valid details
      When I check out with valid customer details
      Then I see the order confirmation
      And my cart is empty
```

| Element | Purpose | Rules |
|---------|---------|-------|
| `Feature:` | Names the business capability | Short noun phrase, no "Test"/"Verify"/app name. Follow with the user story (**As a / I want / So that**) |
| `Background:` | Shared **preconditions** for every scenario in the file (or in the `Rule`) | `Given` steps only, ≤ 4 steps, nothing the reader must remember to understand a scenario. If only some scenarios need it, don't use Background |
| `Rule:` | Groups scenarios that illustrate one business rule | Phrase it as the rule itself. Use it when a feature has more than one rule. A Rule may have its own Background |
| `Scenario:` | One concrete example of one behaviour | Title states the **behaviour and outcome**, unique within the file |
| `Scenario Outline:` + `Examples:` | The same behaviour across varied data | Name each Examples block (`Examples: Missing details`). Keep tables ≤ ~10 rows. Each row must be a meaningful, distinct case |
| Data table | Structured input to one step | Header row, aligned pipes. Prefer it over long `And` chains |
| Doc string (`"""`) | Multi-line text input | Only for real multi-line content (an address, a message body) |
| `# comment` | Notes for maintainers | Rare. Prefer clearer step wording over comments |

## Writing rules

### 1. Declarative, not imperative

Describe **what** the user achieves, not **how** they click. UI details belong in step definitions and page objects. This is the most important rule: imperative scenarios break on every UI change and hide the business intent.

```gherkin
# ❌ Imperative - scripts the UI
When I enter username "standard_user"
And I enter password "secret_sauce"
And I click the login button
Then I should be redirected to the products page

# ✅ Declarative - states the behaviour
When I log in as a "standard" user
Then I see the product catalogue
```

Keep a few low-level UI steps only where the UI itself is the behaviour under test, for example the exact field validation messages on the login form.

### 2. Given / When / Then mean different things

| Keyword | Meaning | Tense & content |
|---------|---------|-----------------|
| `Given` | Context: state of the world **before** the action | Past/present state: "Given my cart contains 2 items". Set up as fast as possible; it is not the thing under test |
| `When` | The **one** action or event under test | Present tense, user intent: "When I remove the backpack from my cart" |
| `Then` | Observable **outcome** the user or business cares about | "Then my cart shows 1 item". Never an action, never an internal detail (DB rows, CSS classes) |
| `And` / `But` | Continue the previous keyword | `But` for a contrasting outcome: "But the bike light is still in my cart" |

- **One `When` per scenario.** Two `When`s usually means two scenarios.
- **Every scenario ends with at least one `Then`.**
- Never use `Given` to perform the action being tested, and never use `Then` to perform an action.

### 3. Step phrasing

- **One point of view per project.** This framework uses first person ("I …"). Don't mix it with "the user …".
- Use the **domain vocabulary** of the business (cart, order, shopper), not tech terms (div, endpoint, modal), and spell things the same way everywhere.
- **Quote literal parameters** (`"Sauce Labs Backpack"`); leave Scenario Outline placeholders bare when they form a phrase (`without a <field>`) and quoted when they are values (`"<error>"`).
- Write lowercase after the keyword: `And the error message …`, not `And The error message …`.
- Write each step to be **reusable** but specific: `When I add "<product>" to my cart`, not `When I add the backpack to my cart` and `When I add the bike light to my cart`.
- Don't use a placeholder to switch **which step** runs (`Then I should <result>`). Each row then matches a different step definition, which hides the logic. Use a placeholder for data, or split the outline.

### 4. Scenarios are independent

- Each scenario must pass when run **alone** and in **any order**. Never rely on state left by a previous scenario.
- Set up all state in `Given`/`Background`. Clean-up belongs in hooks (`environment.py`), not in steps.

### 5. Test data

- Put **examples that explain the rule** in the feature file. Keep bulk or generated data in `test_data/` and load it in the step definitions.
- **No secrets or real credentials in feature files.** Refer to a **role** ("standard" user, "locked out" user) and resolve the credentials from `config/config.py` / environment variables.
- Use realistic but obviously fake personal data ("Jane Doe", "12345").

### 6. Tags

Tags drive CI selection (see the `cicd-pipeline` skill), so use a fixed vocabulary:

| Tag | Meaning | Placement |
|-----|---------|-----------|
| `@smoke` | Critical happy path, runs on every PR, < 5 min total | Scenario |
| `@regression` | Full regression suite | Scenario or Feature |
| `@critical` | Business-critical (money, orders, access) | Scenario |
| `@negative` | Error, validation and edge-case paths | Scenario |
| `@<capability>` | Feature area: `@login`, `@cart`, `@checkout` | Feature |
| `@JIRA-123` | Traceability to a story or defect | Scenario |
| `@wip` | Work in progress, excluded from CI | Scenario |
| `@skip` | Disabled. Must carry a comment saying why and a ticket | Scenario |
| `@flaky` | Quarantined, runs in a non-blocking job | Scenario |

- Lowercase, hyphenated, no spaces. Feature-level tags are inherited by every scenario, so don't repeat them.
- Every scenario has at least one execution tag (`@smoke` or `@regression`).
- Select with tag expressions: `behave --tags "@smoke and not @wip"`.

## Anti-patterns

| ❌ Avoid | ✅ Instead |
|---------|-----------|
| Click-by-click UI scripts | Declarative intent steps (rule 1) |
| `Scenario: Test 1`, `Verify login` | A title that states behaviour and outcome: `Locked-out user cannot log in` |
| Several `When`/`Then` cycles in one scenario | One behaviour per scenario |
| Five near-identical scenarios that differ only by data | One `Scenario Outline` with a named `Examples` table |
| A huge Background, or one that some scenarios don't need | Short `Given`-only Background, or explicit `Given`s per scenario |
| `Then` checks implementation (`the API returns 200`, `the div is visible`) | `Then` checks the user-visible outcome |
| Scenario depends on the previous one | Independent setup in `Given` |
| Hard-coded passwords and tokens | Roles resolved from config |
| `Then I should <result>` switching between steps | Data-only placeholders, or separate outlines |
| `And I wait 5 seconds` | Waits live in page objects (explicit waits) |
| Inconsistent synonyms (log in / sign in / login) | One term per concept, matching the product |

## Review checklist

- [ ] File name is lowercase kebab-case and describes a capability
- [ ] Feature has a title and an As a / I want / So that story
- [ ] Background holds only shared `Given` preconditions, ≤ 4 steps
- [ ] Each scenario title states behaviour and outcome, and is unique
- [ ] Steps are declarative, in business language, with a consistent point of view
- [ ] Exactly one `When`, at least one `Then`, and each `Then` checks a visible outcome
- [ ] 3–7 steps per scenario
- [ ] Repeated data variations use `Scenario Outline` with named `Examples`
- [ ] No secrets in the file; users are referred to by role
- [ ] Scenarios are independent and can run in any order
- [ ] Tags come from the agreed vocabulary, and each scenario has `@smoke` or `@regression`
- [ ] 2-space indent, aligned tables, no trailing whitespace
- [ ] `behave --dry-run` passes, with existing steps reused where possible

## Notes on this repo's current feature files

Use these as refactoring targets when the user asks to clean up existing features. Don't rewrite them unasked, because steps would need to change too.

- All four features are imperative (`I enter username …`, `I click the login button`), and no scenario has tags. `@smoke` CI stages select nothing until tags are added.
- `login.feature` uses `Then I should <result>`, a placeholder that switches step meaning.
- Several steps start with a capital after `And` (`And The error message should contain …`).
- Credentials are hard-coded in steps (`password "secret_sauce"`). These are public demo values, but the pattern should not spread.
- `checkout.feature` has a 7-step Background, which is longer than recommended. Collapse it into declarative steps (`Given my cart contains …`).
