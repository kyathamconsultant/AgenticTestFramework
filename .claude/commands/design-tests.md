---
description: Risk-based test design for a feature (qa-analyst-agent) → specs/<feature>-risk-analysis.md
argument-hint: <feature name or description>
---

Delegate to the **qa-analyst-agent** subagent (`.claude/agents/qa-analyst-agent.md`).

The agent loads these skills itself:
- `.claude/skills/application-domain/SKILL.md`: risk categories (primary)
- `.claude/skills/cucumber-feature-file/SKILL.md`: Gherkin-ready scenario wording and tags

Context: read `CLAUDE.md` and `.claude/ARCHITECTURE.md` (artifact contract, gate G1).

Feature to analyse: $ARGUMENTS

Deliverable: `specs/<feature>-risk-analysis.md` in the agent's Output Structure, plus a short summary (risk counts by level, number of test cases, High risks covered). Design only: no code, no test runs.
