---
name: test-code-review
description: Review code changes in this Python Behave + Playwright test automation framework to industry standards - correctness, security, test reliability (waits, assertions, flakiness), Page Object Model design, step definitions, feature files, CI config, maintainability, and PEP 8 - and report findings by severity with file:line references and concrete fixes. Use when asked to review a diff, branch, pull request, file, or the framework, or to check code before committing or merging.
license: Proprietary - internal QA team use
compatibility: Python 3.8+ repo using Behave, Playwright (sync API) and Allure. Uses git for diffs; ruff is optional for automated checks.
metadata:
  author: QA Team
  version: "1.0"
  updated: "2026-10-30"
  category: code-quality
---

# Code Review Standards

**Goal:** approve a change once it clearly improves the overall health of the codebase, even if it isn't perfect. Block it for real defects, not for preferences.

## Workflow

1. **Scope the change.**
   - Branch or PR: `git diff main...HEAD` and `git log main..HEAD --oneline`.
   - Uncommitted work: `git diff` plus `git diff --staged`.
   - A named file or folder: review it as it stands.
   - Read the PR description or ask what the change is meant to do. You can't judge correctness without knowing the intent.
2. **Run the cheap automated checks first,** and don't report by hand what a tool already catches:
   ```bash
   ruff check . --select E9,F63,F7,F82   # syntax errors, undefined names
   ruff check <changed files>            # full lint on the change only
   behave --dry-run                      # Gherkin parses, no undefined steps
   ```
   If ruff isn't installed, say so rather than skipping silently.
3. **Read the whole change in context.** Open the surrounding code, the callers and the related page object, step and feature, not just the diff lines.
4. **Review in [priority order](#review-priorities).** Spend most of the time on correctness and reliability, and the least on style.
5. **Verify each finding before reporting it.** Trace the code path or run the scenario: `behave features/x.feature -n "<scenario>"`. Drop anything you can't substantiate, or label it clearly as a question.
6. **Report** in the [output format](#output-format), most severe first.

## Review priorities

| # | Area | Ask |
|---|------|-----|
| 1 | **Correctness** | Does it do what it claims? Can a test pass while the feature is broken (false green)? Edge cases, empty or None values, off-by-one errors, wrong comparisons |
| 2 | **Security** | Secrets in code or logs? Credentials committed? Unsafe input handling? Vulnerable dependencies? |
| 3 | **Test reliability** | Will it be flaky? Hard sleeps, race conditions, order dependence, shared state, brittle selectors |
| 4 | **Design** | Does it follow POM and keep the layers apart? Is it in the right place? Does it duplicate existing helpers? |
| 5 | **Maintainability** | Readable names, small functions, clear errors, no dead code, docs updated |
| 6 | **Style** | PEP 8 and project conventions. Lowest priority; leave it to linters where possible |

## Severity levels

| Severity | Meaning | Merge? |
|----------|---------|--------|
| 🔴 **Blocker** | Bug, false-green test, security issue, data loss, or a broken build or CI | Must fix |
| 🟠 **Major** | Likely flakiness, a design problem that will spread, a missing test for new logic, swallowed errors | Fix before merge unless a follow-up ticket is agreed |
| 🟡 **Minor** | Maintainability or readability improvement with clear value | Author's call |
| ⚪ **Nit** | Style or preference | Optional; prefix with `nit:` |
| 💬 **Question** | You need information to judge | Answer before merge |

Also call out things done well (`praise:`). Reviews that only list faults teach less.

## Checklists

### Python (all code)

- [ ] PEP 8, `snake_case`, lines ≤ 100 characters (see `CLAUDE.md`), imports grouped stdlib / third-party / local
- [ ] Descriptive names. No single-letter variables outside comprehensions
- [ ] Functions do one thing (roughly ≤ 30 lines). No deep nesting (early returns instead)
- [ ] **No bare `except:`. Catch only exceptions you handle.** Never catch and return `False`/`None` in a way that hides the original error (see [repo findings](#known-issues-in-this-repo))
- [ ] No mutable default arguments (`def f(items=[])`)
- [ ] `pathlib` for paths. No hard-coded OS-specific separators or absolute paths
- [ ] Logging through `get_logger(__name__)`, never `print`. Correct levels (`error` for failures, `debug` for noise)
- [ ] **Nothing sensitive in logs**: passwords, tokens, personal data
- [ ] No commented-out code, unused imports or unused variables
- [ ] Type hints on new public functions (encouraged)
- [ ] Comments explain *why*, not *what*

### Page objects (`pages/`)

- [ ] Selectors are **class constants**, defined once, never inline in methods or steps
- [ ] Selector priority: `data-test` attribute > role/label > id > CSS. No XPath on text or position, no auto-generated classes
- [ ] Pages expose **intent** methods (`login(user)`, `add_to_cart(name)`), not raw clicks
- [ ] No assertions inside page objects. They return state (`get_error_message()`) and steps assert on it. Exception: guarding that the right page loaded
- [ ] Inherits `BasePage` and reuses its helpers instead of re-implementing them
- [ ] Waits are explicit (`wait_for_selector`, `expect(...)`, locator auto-wait). **No `time.sleep` / `wait_for_timeout`**
- [ ] Timeouts come from `Config`, not magic numbers

### Step definitions (`features/steps/`)

- [ ] Steps are thin: they call page objects and assert. No selectors, no Playwright calls
- [ ] **Assertions carry a useful message** with expected vs. actual: `assert actual == expected, f"Cart count: expected {expected}, got {actual}"`
- [ ] Assertions check the **outcome**, not the success of an action. `assert page.click_x()` only proves the click didn't throw
- [ ] No duplicate step patterns across files (Behave raises `AmbiguousStep`). Reuse existing steps
- [ ] State is shared via `context` attributes that are set before they are read, and nothing leaks between scenarios
- [ ] Parameters are typed (`{count:d}`) instead of casting strings by hand

### Feature files (`features/*.feature`)

Review against the `cucumber-feature-file` skill:
- Declarative steps
- One `When` per scenario
- Tags from the agreed vocabulary
- No credentials in the file
- Independent scenarios

### Hooks, config & data

- [ ] `environment.py` cleans up browser, context and Playwright in every case, including after failures, and screenshots on failure
- [ ] New settings go through `config/config.py` with a safe default and are documented in `CLAUDE.md` or `.env.example`
- [ ] **No secrets committed.** `.env` stays local. CI uses its secret store
- [ ] Test data lives in `test_data/`, read through `utilities/data_reader.py`
- [ ] New dependencies are justified, pinned to a minimum version, and actually installable (`pip index versions <pkg>`)

### CI / pipelines

Review against the `cicd-pipeline` skill, especially:
- Least-privilege permissions
- No inline `${{ }}` in `run:`
- Timeouts
- Artifacts uploaded on `always()`
- A zero-test guard

### The change as a whole

- [ ] Focused: one concern per PR, ideally under ~400 changed lines. Suggest splitting larger PRs
- [ ] New behaviour has a scenario. Bug fixes have a test that fails without the fix
- [ ] Docs (`CLAUDE.md`, `README.md`) are updated when behaviour, commands or config change
- [ ] No generated files committed (`results/`, `__pycache__/`, `allure-report/`)

## Writing review comments

- **Be specific:** quote the line, say what's wrong, why it matters, and how to fix it. Include a code suggestion when the fix is small.
- **Comment on the code, not the person:** "this function swallows the timeout", not "you forgot".
- **Separate must-fix from optional** with the severity labels. Don't make the author guess.
- **Ask when unsure:** "Is it intended that…?" beats a confident wrong claim.
- **Don't pile on:** report a repeated pattern once, list where else it occurs, and don't repeat the comment on every line.
- **Stay in scope:** pre-existing problems the change didn't touch go in a separate "Outside this change" note, and never block the PR.

## Output format

```markdown
## Code Review: <branch / PR / files>

**Verdict:** ✅ Approve | 💬 Approve with comments | ❌ Request changes
**Summary:** <1–3 sentences: what the change does and its overall quality>
**Checks run:** ruff ✅ | behave --dry-run ✅ | scenarios executed: <which, or "not run">

### Findings

#### 🔴 Blocker: <short title>
`path/to/file.py:42`: <what is wrong and the concrete failure scenario>
**Fix:** <specific change, with a snippet if small>

#### 🟠 Major: …
#### 🟡 Minor: …
#### ⚪ nit: …
#### 💬 Question: …

### Done well
- <specific praise>

### Outside this change (not blocking)
- <pre-existing issues noticed nearby>
```

Verdict rules:
- Any Blocker → **Request changes**.
- Majors only → **Request changes**, unless a follow-up ticket is agreed.
- Otherwise → **Approve** (with comments if there are any).

## Known issues in this repo

These patterns already exist (verified on 2026-10-30). Flag new code that copies them. Mention the existing occurrences only as "Outside this change" unless the user asks for a full-framework review.

| Pattern | Where | Why it matters | Preferred |
|---------|-------|----------------|-----------|
| `except Exception` → `return False`/`None` | `pages/base_page.py` (10+ methods) | Discards Playwright's error (timeouts, the selector that failed). Steps then fail with a vague `"Failed to click"` | Let exceptions propagate, or re-raise with context: `raise AssertionError(f"…{selector}") from e` |
| `fill_input` logs the value | `pages/base_page.py:55` | Writes passwords to console, `results/logs/` and CI logs | Log the selector only, or mask values for password fields |
| `time.sleep` in `implicit_wait` | `utilities/wait_utils.py:71` | Hard sleep: slow and flaky | Explicit waits on a condition |
| `assert page.click_x(), "Failed to click…"` | `features/steps/*_steps.py` | Asserts the action, not the outcome. Only meaningful because of the swallowed exceptions above | Call the action, then assert the resulting state |
| `.env` tracked in git | repo root | Credentials in version control | `.gitignore` it and commit `.env.example` |
