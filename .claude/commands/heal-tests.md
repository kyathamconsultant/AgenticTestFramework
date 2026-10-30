---
description: Diagnose and fix failing Behave scenarios (playwright-test-healer)
argument-hint: "[feature file | scenario name | blank = whole suite]"
---

Target: $ARGUMENTS (if blank, run `HEADLESS=true behave` for the whole suite and heal what fails)

1. Run the target headless and collect the failures:
   - `HEADLESS=true behave <feature>`
   - Use `-n "<scenario>"` for a single scenario.
2. Delegate each failing feature to the **playwright-test-healer** subagent (`.claude/agents/playwright-test-healer.md`). Pass the failing output and the feature id. Features can be healed in parallel when they don't share page objects or steps.
3. The healer loads these skills itself:
   - `.claude/skills/playwright-test-automation/SKILL.md`: fix standards (primary)
   - `.claude/skills/cucumber-feature-file/SKILL.md`: keep scenario intent
   - `.claude/skills/test-code-review/SKILL.md`: self-check
   - `.claude/skills/cicd-pipeline/references/STANDARDS.md`: flaky-test policy
4. Re-run the whole target to confirm there are no regressions.

Report:
- Scenarios healed, with their root-cause categories (A–F)
- Application defects found (these must not be masked)
- Anything escalated after 3 rounds
- Paths of the healing logs

Do not commit unless asked.
