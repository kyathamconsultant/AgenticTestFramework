# Agentic Test Automation Architecture

**Version:** 2.0 (2026-10-30)
**Stack:** Python 3.8+ · Behave (Gherkin) · Playwright sync API · Allure · Playwright MCP (`browser_*` tools)

This document defines how the Claude skills, agents and commands in `.claude/` work together. It is the single source of truth for who does what, which standards apply, and which files pass between stages.

---

## 1. Design principles

| # | Principle | Consequence |
|---|-----------|-------------|
| 1 | **One stack.** The framework is Python Behave. | No agent, skill or command may generate TypeScript, `.spec.ts`, `playwright.config.ts` or `npm` test scripts |
| 2 | **Skills own standards; agents own workflow.** | Agents *load* skills and never copy their rules. A standard changes in exactly one file |
| 3 | **Commands are entry points; the main session orchestrates.** | Claude Code subagents cannot start other subagents, so multi-agent pipelines are driven from the main session by a command |
| 4 | **File-based handoffs.** | Each stage writes an artifact at a fixed path, and the next stage reads it. Runs are resumable and reviewable |
| 5 | **Never guess selectors.** | Selectors come from live DOM inspection through the Playwright MCP `browser_*` tools |
| 6 | **Verify before claiming.** | Every stage that changes code ends with `behave --dry-run` and a real `behave` run |
| 7 | **Quality gate before done.** | Generated or healed code goes through the test-code-review skill before it is reported as complete |

---

## 2. Layers

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ COMMANDS (entry points)                                .claude/commands/     │
│  /design-tests  /generate-playwright-tests  /heal-tests  /review-tests       │
│  /setup-pipeline                                                             │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ invoke (main session)
┌───────────────▼──────────────────────────────────────────────────────────────┐
│ AGENTS (workflow + handoffs)                           .claude/agents/       │
│  playwright-automation-agent (orchestrator, runs in the main session)        │
│  qa-analyst-agent ▸ playwright-test-planner ▸ playwright-test-generator      │
│  ▸ playwright-test-healer ▸ test-code-reviewer                               │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ load
┌───────────────▼──────────────────────────────────────────────────────────────┐
│ SKILLS (standards + knowledge)                         .claude/skills/       │
│  application-domain   cucumber-feature-file   playwright-test-automation     │
│  test-code-review     cicd-pipeline                                          │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ apply to
┌───────────────▼──────────────────────────────────────────────────────────────┐
│ FRAMEWORK (Python)                                                           │
│  features/*.feature  features/steps/*_steps.py  pages/*_page.py              │
│  test_data/  config/config.py  utilities/  environment.py  behave.ini        │
│  .github/workflows/e2e-tests.yml                                             │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Skills: the knowledge layer

| Skill | Owns | Path |
|-------|------|------|
| `application-domain` | E-commerce risk categories (financial, inventory, fraud, validation, data integrity, compliance) and risk-based test design | `.claude/skills/application-domain/SKILL.md` |
| `cucumber-feature-file` | Gherkin standards: declarative steps, Given/When/Then, Background/Rule/Outline, tags, naming | `.claude/skills/cucumber-feature-file/SKILL.md` |
| `playwright-test-automation` | Python implementation standards: locators, POM, step definitions, assertions, waits, hooks, data, Allure | `.claude/skills/playwright-test-automation/SKILL.md` |
| `test-code-review` | Review priorities, severity levels, checklists, report format, known repo issues | `.claude/skills/test-code-review/SKILL.md` |
| `cicd-pipeline` | Pipeline standards, preflight, templates, runner script | `.claude/skills/cicd-pipeline/SKILL.md` |

The skill was renamed from `code-review` to `test-code-review` so that it doesn't clash with Claude Code's built-in `/code-review`.

### Agent × skill matrix

● = primary (load before starting) · ◐ = consult for a specific step · – = not used

| Agent | application-domain | cucumber-feature-file | playwright-test-automation | test-code-review | cicd-pipeline |
|-------|:-:|:-:|:-:|:-:|:-:|
| playwright-automation-agent (orchestrator) | ● | ● | ● | ● | ◐ (if CI is touched) |
| qa-analyst-agent | ● | ◐ (scenario wording) | – | – | – |
| playwright-test-planner | ◐ (risk priority) | ◐ (scenario shape) | ● (locator strategy) | – | – |
| playwright-test-generator | ◐ (financial assertions) | ● | ● | ◐ (self-check) | – |
| playwright-test-healer | – | ◐ (preserve intent) | ● | ◐ (self-check) | ◐ (flaky policy) |
| test-code-reviewer | ◐ (risk coverage) | ● | ● | ● | ◐ (pipeline files) |

### Command × skill/agent matrix

| Command | Agent(s) | Skills loaded directly |
|---------|----------|------------------------|
| `/design-tests <feature>` | qa-analyst-agent | application-domain, cucumber-feature-file |
| `/generate-playwright-tests <feature>` | orchestrator → analyst (optional) → planner → generator → healer (on failure) → reviewer | all five via the agents |
| `/heal-tests [feature or scenario]` | playwright-test-healer | playwright-test-automation |
| `/review-tests [target]` | test-code-reviewer | test-code-review |
| `/setup-pipeline [platform]` | – (main session) | cicd-pipeline |

---

## 4. Agents: the workflow layer

| Agent | Role | Model | Input | Output artifact |
|-------|------|-------|-------|-----------------|
| `playwright-automation-agent` | Orchestrator. Sequences the stages, checks each artifact, enforces gates | opus | Feature name/description from the command | Final summary in chat |
| `qa-analyst-agent` | Risk-based test design | opus | Feature description, requirements | `specs/<feature>-risk-analysis.md` |
| `playwright-test-planner` | Live exploration with MCP, scenarios, selector inventory | sonnet | Risk analysis (if any), app URL | `specs/<feature>-test-plan.md` |
| `playwright-test-generator` | Writes Gherkin, steps, page objects and data in Python | sonnet | Test plan | `features/<feature>.feature`, `features/steps/<feature>_steps.py`, `pages/<feature>_page.py`, `test_data/<feature>_data.json` |
| `playwright-test-healer` | Diagnoses and fixes failing scenarios | sonnet | Failing `behave` output | Code fixes + `specs/<feature>-healing-log.md` |
| `test-code-reviewer` | Read-only quality gate | sonnet | Changed files / diff | Review report (chat) |

### End-to-end flow (`/generate-playwright-tests`)

```
 main session (orchestrator instructions)
   │
   ├─1─▶ qa-analyst-agent ─────────▶ specs/<f>-risk-analysis.md     (skip if it exists and is current)
   │
   ├─2─▶ playwright-test-planner ──▶ specs/<f>-test-plan.md         (MCP browser_* exploration)
   │        gate: every scenario has steps, expected results and live selectors
   │
   ├─3─▶ playwright-test-generator ▶ .feature + _steps.py + _page.py + _data.json
   │        gate: behave --dry-run passes (no undefined or ambiguous steps)
   │
   ├─4─▶ run: behave features/<f>.feature  (HEADLESS=true)
   │        ├─ pass ──────────────────────────────┐
   │        └─ fail ─▶ playwright-test-healer ─▶ re-run (max 3 rounds, then escalate)
   │                                              │
   ├─5─▶ test-code-reviewer ◀─────────────────────┘
   │        gate: no Blocker or Major findings (fix via generator/healer, then re-review)
   │
   └─6─▶ summary to user: files, scenarios, pass/fail, review verdict, open risks
```

---

## 5. Artifact contract

| Artifact | Path | Written by | Read by |
|----------|------|------------|---------|
| Risk analysis | `specs/<feature>-risk-analysis.md` | qa-analyst-agent | planner, generator, reviewer |
| Test plan + selector inventory | `specs/<feature>-test-plan.md` | planner | generator, healer |
| Feature file | `features/<feature>.feature` | generator | healer, reviewer, CI |
| Step definitions | `features/steps/<feature_snake>_steps.py` | generator | healer, reviewer |
| Page object | `pages/<page_snake>_page.py` | generator | healer, reviewer |
| Test data | `test_data/<feature_snake>_data.json` (or `.csv`) | generator | steps |
| Healing log | `specs/<feature>-healing-log.md` | healer | reviewer, team |
| Run results | `results/` (Allure, JUnit, logs, screenshots) | behave / CI | healer, CI report |

Naming:
- `<feature>` is lowercase kebab-case (`order-checkout`).
- `<feature_snake>` is the same name in snake_case (`order_checkout`), because Python module names cannot contain hyphens.

---

## 6. Tooling rules

| Need | Use | Don't use |
|------|-----|-----------|
| Explore the app and discover selectors | `mcp__playwright-test__browser_navigate`, `browser_snapshot`, `browser_click`, `browser_fill_form`, `browser_generate_locator`, `browser_verify_*`, `browser_take_screenshot` | Guessing selectors from memory |
| Run tests | `behave …` (or `bash .claude/skills/cicd-pipeline/scripts/run_tests.sh`) via Bash | `npx playwright test`, `mcp__playwright-test__test_run`, `test_debug`, `generator_write_test`, `planner_setup_page` (these target TypeScript `@playwright/test` specs) |
| Check Gherkin and step binding | `behave --dry-run`, `behave --steps-catalog` | – |
| Lint | `ruff check` | – |

`seed.spec.ts` and the `npx playwright run-test-mcp-server` entry in `.mcp.json` exist only to provide the MCP browser tools. No tests are written in TypeScript.

---

## 7. Quality gates

| Gate | Stage | Check | On failure |
|------|-------|-------|-----------|
| G1 Coverage | after analyst | Every high-risk item maps to at least one scenario | Analyst revises |
| G2 Plan | after planner | Each scenario has steps, expected results and live selectors | Planner re-explores |
| G3 Binding | after generator | `behave --dry-run` reports no undefined or ambiguous steps | Generator fixes |
| G4 Execution | after run | All scenarios pass headless | Healer, max 3 rounds, then escalate to user |
| G5 Review | after reviewer | No Blocker or Major findings | Fix, then re-review |
| G6 CI | on push/PR | `.github/workflows/e2e-tests.yml` passes | See cicd-pipeline skill |

---

## 8. Extending the system

- **New standard:** add it to the owning skill only. Agents pick it up automatically.
- **New agent:** add it to `.claude/agents/` with a "Skills" table at the top, then add a row to the matrices in section 3 and the artifact contract in section 5.
- **New command:** keep it short. It names the agent(s), the skills and the arguments, and defers everything else.
- **Skill format:** follows the Agent Skills spec. Frontmatter has `name` (same as the folder), `description` (what it does and when to use it), and optionally `license`, `compatibility` and `metadata`. Keep the body under 500 lines and put detail in `references/`, `scripts/` and `assets/`.
