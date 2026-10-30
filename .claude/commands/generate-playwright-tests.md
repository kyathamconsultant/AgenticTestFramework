---
description: End-to-end automation of a feature - analyse, explore, generate Python Behave tests, heal, review
argument-hint: <feature name or description>
---

Read `.claude/agents/playwright-automation-agent.md` and act as that orchestrator **in this main session**, so you can delegate to the specialist agents with the Agent tool.

Feature to automate: $ARGUMENTS

Before starting, read:
- `CLAUDE.md`: project context and stack
- `.claude/ARCHITECTURE.md`: stages, artifact contract, gates G1–G5, tooling rules

Run the stages exactly as the orchestrator defines them:

| # | Stage | Agent | Skills the agent loads |
|---|-------|-------|------------------------|
| 1 | Risk analysis (skip if current) | `qa-analyst-agent` | application-domain, cucumber-feature-file |
| 2 | Live exploration & test plan (MCP `browser_*` tools) | `playwright-test-planner` | playwright-test-automation, application-domain, cucumber-feature-file |
| 3 | Generate feature, steps, page objects, data | `playwright-test-generator` | cucumber-feature-file, playwright-test-automation, application-domain, test-code-review |
| 4 | Run `HEADLESS=true behave features/<feature>.feature`; heal failures (max 3 rounds) | `playwright-test-healer` | playwright-test-automation, cucumber-feature-file, test-code-review, cicd-pipeline (flaky policy) |
| 5 | Quality gate | `test-code-reviewer` | test-code-review, cucumber-feature-file, playwright-test-automation, application-domain, cicd-pipeline |

Output files (Python Behave only, no TypeScript):

| Artifact | Path |
|----------|------|
| Risk analysis | `specs/<feature>-risk-analysis.md` |
| Test plan | `specs/<feature>-test-plan.md` |
| Feature file | `features/<feature>.feature` |
| Step definitions | `features/steps/<feature_snake>_steps.py` |
| Page objects | `pages/<page_snake>_page.py` |
| Test data | `test_data/<feature_snake>_data.json` |
| Healing log | `specs/<feature>-healing-log.md` (only if healing ran) |

Finish with the orchestrator's final report. Do not commit or push unless asked.
