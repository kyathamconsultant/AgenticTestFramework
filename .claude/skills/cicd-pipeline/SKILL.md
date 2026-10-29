---
name: cicd-pipeline
description: Create, review, or fix CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins) for the Behave + Playwright + Allure test framework - lint gates, cross-browser matrix, caching, secrets, flaky-test reruns, and Allure report publishing. Use when asked to add, set up, harden, or debug a pipeline, workflow, Jenkinsfile, or .gitlab-ci.yml, or when tests pass locally but fail in CI.
license: Proprietary - internal QA team use
compatibility: Requires bash, Python 3.8+, behave, playwright and allure-behave. Report generation in CI needs Java 17+ and network access to download the Allure CLI.
metadata:
  author: QA Team
  version: "1.0"
  updated: "2026-10-29"
  category: devops-test-automation
---

# CI/CD Pipeline Skill

Build industry-standard pipelines for the SauceDemo Behave + Playwright + Allure framework. All file paths below are relative to this skill's directory.

## Layout

```
cicd-pipeline/
├── SKILL.md                      # This file: workflow + architecture
├── scripts/
│   ├── run_tests.sh              # Single CI entrypoint used by every platform
│   └── label_allure_results.py   # Tags Allure results per browser for merged reports
├── references/
│   ├── PREFLIGHT.md              # Repo checks that must pass before CI works
│   ├── STANDARDS.md              # Core standards, quality gates, secrets, flaky policy, anti-patterns
│   └── PLATFORMS.md              # Per-platform setup, required plugins, validation commands
└── assets/
    ├── github-actions-e2e.yml    # → .github/workflows/e2e-tests.yml
    ├── gitlab-ci.yml             # → .gitlab-ci.yml
    └── Jenkinsfile               # → Jenkinsfile
```

## Workflow

1. **Detect the platform.** Look for `.github/workflows/`, `.gitlab-ci.yml` or `Jenkinsfile`. If none exists and the user named no platform, ask. Do not generate all three by default.
2. **Run preflight.** Work through [references/PREFLIGHT.md](references/PREFLIGHT.md). Report blockers and fix them only with the user's approval. Two blockers are known in this repo (`requirements.txt`, `behave.ini`).
3. **Copy the template** from `assets/` to its target location (see Layout).
4. **Adapt it:** default branch, Python version, browsers, schedule, secret names. Map only secrets that exist (see "Secrets & configuration" in [references/STANDARDS.md](references/STANDARDS.md)).
5. **Validate statically** with the platform linter listed under "Static validation" in [references/PLATFORMS.md](references/PLATFORMS.md).
6. **Validate the runner locally:**
   ```bash
   HEADLESS=true FEATURES=features/login.feature bash .claude/skills/cicd-pipeline/scripts/run_tests.sh
   ```
   It must pass locally before it can pass in CI.
7. **Report to the user:**
   - The files you created
   - The one-time setup they must do (secrets, Pages, branch protection, from [references/PLATFORMS.md](references/PLATFORMS.md))
   - Anything you could not verify

When **reviewing** an existing pipeline, check it against the Review checklist below and [references/STANDARDS.md](references/STANDARDS.md).

## Architecture

```
 Trigger ──▶ Lint & Parse ──▶ E2E (matrix per browser) ──▶ Report ──────▶ Publish
 PR/push     ruff (fatal)     run_tests.sh                 merge results   Pages
 nightly     behave dry-run   JUnit + Allure + shots       Allure + hist   (main only)
 manual      pip-audit        fail-fast: false             if: always()
```

| Trigger | Browsers | Scope | Purpose |
|---------|----------|-------|---------|
| Pull request | chromium | Full suite (or `@smoke` once tagged) | Fast merge gate |
| Push to `main` | chromium | Full suite | Post-merge check + publish report |
| Nightly schedule | chromium, firefox, webkit | Full suite | Cross-browser regression |
| Manual | user-selected | user-selected tags | Ad-hoc / debugging |

## Runner script

`scripts/run_tests.sh`:
- Exports `HEADLESS=true`
- Writes Allure results, JUnit XML and a rerun file under `results/`
- Re-runs failed scenarios once and records them in `results/flaky-candidates.txt`
- Calls `scripts/label_allure_results.py` so a merged cross-browser report keeps the browsers apart instead of showing them as retries
- Exits non-zero only on real failures

| Env var | Default | Example |
|---------|---------|---------|
| `BROWSER` | `chromium` | `firefox` |
| `TAGS` | *(all)* | `@smoke and not @wip` |
| `FEATURES` | `features` | `features/login.feature` |
| `RERUN_FAILED` | `1` | `0` to disable |
| `RESULTS_DIR` | `results` | `out/run-42` |

## Review checklist

- [ ] Preflight blockers are resolved
- [ ] Lint/parse runs before browser jobs, and E2E depends on it
- [ ] Matrix uses `fail-fast: false`
- [ ] Every job has a timeout
- [ ] Superseded runs are cancelled
- [ ] Top-level permissions are read-only and widened per job only
- [ ] No secrets in YAML or in a committed `.env`; unset secrets are not mapped
- [ ] User inputs reach shell steps via `env:`, never inline `${{ }}`
- [ ] Pip and Playwright browser caches are keyed correctly
- [ ] Artifacts upload on `always()`, with retention set
- [ ] JUnit is published to the native test tab
- [ ] Allure report is generated with history
- [ ] Zero-test guard is present
- [ ] Rerun is limited to 1, and flaky candidates are surfaced
- [ ] Report is published only from the default branch
- [ ] Branch protection requires the lint and chromium E2E checks
