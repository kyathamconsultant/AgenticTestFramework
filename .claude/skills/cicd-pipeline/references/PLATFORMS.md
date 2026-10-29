# Platform Setup Notes

## Contents
- [GitHub Actions](#github-actions)
- [GitLab CI](#gitlab-ci)
- [Jenkins](#jenkins)
- [Static validation](#static-validation)

## GitHub Actions

Template: `assets/github-actions-e2e.yml` → `.github/workflows/e2e-tests.yml`

Jobs: `lint` → `plan` (browser matrix) → `e2e` (matrix) → `report` (Allure + summary) → `deploy` (Pages, `main` only)

One-time repo setup the user must do:
- *Settings → Pages → Source: GitHub Actions*
- *Settings → Branches → protect `main`*: require the status checks `Lint & Parse` and `E2E (chromium)`
- *Settings → Secrets and variables → Actions*: add any credential secrets, then uncomment their mapping in the `e2e` job's `env:` block

Allure history is restored from the previously deployed Pages site (`<site>/history/*.json`). The first run has no history, which is expected.

## GitLab CI

Template: `assets/gitlab-ci.yml` → `.gitlab-ci.yml`

Jobs: `lint` + `dependency-audit` → `e2e` (MR/branch, chromium) or `e2e:cross-browser` (schedule, 3 browsers) → `allure-report` → `pages` (default branch)

One-time setup:
- *Settings → CI/CD → Variables*: credentials marked **Masked** and **Protected**
- *Build → Pipeline schedules*: nightly schedule (triggers the cross-browser job)
- For a cross-browser run on demand, use *Run pipeline* with `CROSS_BROWSER=true`

The GitLab Pages job must be named `pages` and publish `public/`.

## Jenkins

Template: `assets/Jenkinsfile` → `Jenkinsfile`

Required plugins:
- Pipeline
- Docker Pipeline
- JUnit
- Allure Jenkins Plugin (configure the Allure tool under *Global Tool Configuration*)
- Timestamper

Notes:
- Chromium always runs. Firefox and WebKit run when `CROSS_BROWSER=true` or on the nightly cron.
- `--ipc=host` on the Docker agent prevents Chromium crashes caused by the small default `/dev/shm`.
- `junit allowEmptyResults: false` acts as the zero-test guard.
- The Allure plugin keeps report history between builds automatically.
- Credentials: add a *Secret text* credential and uncomment the `withCredentials` block.

## Static validation

| Platform | Command |
|----------|---------|
| GitHub | `actionlint .github/workflows/e2e-tests.yml` |
| GitLab | `glab ci lint`, or *CI/CD → Editor → Validate* |
| Jenkins | `java -jar jenkins-cli.jar -s $JENKINS_URL declarative-linter < Jenkinsfile` |

If the validator is not installed, say so in the report instead of claiming the file is valid.
