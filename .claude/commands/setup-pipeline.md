---
description: Create, update, or review the CI/CD pipeline using the cicd-pipeline skill
argument-hint: "[github | gitlab | jenkins | review]"
---

Request: $ARGUMENTS

Load `.claude/skills/cicd-pipeline/SKILL.md` and follow its Workflow:
1. **Detect the platform.** Use the argument, or look for `.github/workflows/`, `.gitlab-ci.yml` or `Jenkinsfile`. Ask if it's unclear.
2. **Preflight.** Work through `references/PREFLIGHT.md` and report blockers. Fix them only with approval.
3. **Template.** Copy and adapt the matching template from `assets/`.
4. **Validate.** Check statically (`references/PLATFORMS.md`), then run `scripts/run_tests.sh` locally.
5. **Report.** List the files changed and the one-time platform setup the user must do.

For `review`, check the existing pipeline files against the skill's Review checklist and `references/STANDARDS.md`, using the severity format from `.claude/skills/test-code-review/SKILL.md`.

If scenarios gained new tags (`@smoke`, `@flaky`, …), make sure the pipeline's tag expressions select them correctly. Keep the zero-test guard.

Do not commit or push unless asked.
