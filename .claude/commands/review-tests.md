---
description: Review test code to team standards (test-code-reviewer) - severity-ranked report with verdict
argument-hint: "[branch | file/folder | feature | blank = current branch vs main, else uncommitted changes]"
---

Target: $ARGUMENTS

Delegate to the **test-code-reviewer** subagent (`.claude/agents/test-code-reviewer.md`), passing the target. If the target is blank, the reviewer uses:
- `git diff main...HEAD` when the branch has commits ahead of `main`
- otherwise `git diff` plus `git diff --staged`

The reviewer loads these skills itself:
- `.claude/skills/test-code-review/SKILL.md`: review procedure, severities, report format (primary)
- `.claude/skills/cucumber-feature-file/SKILL.md`: feature files
- `.claude/skills/playwright-test-automation/SKILL.md`: pages, steps, hooks
- `.claude/skills/application-domain/SKILL.md`: risk coverage
- `.claude/skills/cicd-pipeline/SKILL.md`: pipeline files

Show the reviewer's report to the user unchanged. If they then ask for fixes, route new-code issues to `playwright-test-generator` and failing or flaky tests to `playwright-test-healer`, then re-review.

(This is the project review. Claude Code's built-in `/code-review` is a separate general-purpose reviewer.)
