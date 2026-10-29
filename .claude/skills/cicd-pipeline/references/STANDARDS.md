# Pipeline Standards

## Contents
- [Core standards](#core-standards)
- [Quality gates](#quality-gates)
- [Secrets & configuration](#secrets--configuration)
- [Flaky test policy](#flaky-test-policy)
- [Anti-patterns](#anti-patterns)

## Core standards

| # | Standard | Why | How |
|---|----------|-----|-----|
| 1 | **One entrypoint script** | CI and local runs stay identical, and switching CI vendors does not mean rewriting how tests run | Every pipeline calls `scripts/run_tests.sh` |
| 2 | **Fail fast on cheap checks** | Don't spend browser minutes on a syntax error | Lint and `behave --dry-run` gate the E2E stage |
| 3 | **`fail-fast: false` in matrices** | One browser failing must not hide the others' results | Matrix strategy setting |
| 4 | **Always collect artifacts** | Failures are the runs you most need evidence from | `if: always()` / `when: always` / `post { always }` |
| 5 | **Headless in CI** | No display on runners | `HEADLESS=true` exported by the runner script |
| 6 | **Cache dependencies** | Faster runs (pip ~30s, browsers ~60s) | Pip cache keyed on `requirements.txt`; browser cache keyed on Playwright version + browser |
| 7 | **Job timeouts** | A hung browser must not burn runner hours | `timeout-minutes` / `timeout:` / `options { timeout }` |
| 8 | **Cancel superseded runs** | Saves capacity on rapid pushes | `concurrency` / `interruptible` / `disableConcurrentBuilds(abortPrevious: true)` |
| 9 | **Least-privilege tokens** | Limits the damage from a compromised step | `permissions: contents: read` at the top level; widen per job |
| 10 | **Secrets from the CI store** | Credentials must never live in git | GitHub Secrets / GitLab masked variables / Jenkins Credentials |
| 11 | **Pin versions** | Reproducible builds | Pin actions to a major version (SHA-pin for high-security repos) and pin the Python, Allure and container images |
| 12 | **Machine-readable results** | Native CI test tabs, PR annotations, trend tracking | JUnit XML **and** Allure results |
| 13 | **Retry once, then report** | Separates flaky from broken without hiding real failures | Rerun-failed in the runner script; flaky list as an artifact |
| 14 | **Report history** | Trends and flaky detection need previous runs | Restore Allure `history/` before generating the report |
| 15 | **Zero-test guard** | A tag filter that matches nothing produces a false green | Fail if JUnit reports 0 test cases |
| 16 | **No inline user input in shell** | Script injection via PR titles or dispatch inputs | Pass `${{ inputs.* }}` / `github.event.*` through `env:` |

## Quality gates

| Gate | Stage | Blocking? |
|------|-------|-----------|
| Python syntax/undefined names (`ruff --select E9,F63,F7,F82`) | Lint | Yes |
| Gherkin parses and all steps are defined (`behave --dry-run`) | Lint | Yes |
| Dependency vulnerabilities (`pip-audit`) | Lint | Non-blocking until the baseline is clean, then blocking |
| All scenarios pass (after one rerun) | E2E | Yes |
| At least one scenario executed | E2E | Yes |
| Flaky scenarios detected | Report | Warning + ticket |

## Secrets & configuration

| Rule | Detail |
|------|--------|
| Never commit secrets | `.env` is for local runs only. CI injects values as env vars, which take precedence over `.env` (`load_dotenv` does not override) |
| Map only the secrets that exist | `Config` uses `os.getenv(KEY, default)`. An empty-string env var overrides the default with `""` |
| Mask in logs | GitHub masks secrets automatically. GitLab needs the variable marked **Masked**. Jenkins masks values bound with `withCredentials` |
| Non-secret config | Use plain pipeline `env`/`variables` for values like `BASE_URL`, `EXPLICIT_WAIT` and `VIEWPORT_*` |
| Per-environment targets | Use GitHub Environments, GitLab environments or Jenkins folders to switch `BASE_URL` (dev/staging/prod), each with its own protected secrets |

## Flaky test policy

1. **Detect.** `run_tests.sh` re-runs failures once. A scenario that passes on rerun is written to `flaky-candidates.txt` and shows as a retry in Allure.
2. **Surface.** The report job lists flaky candidates in the job summary. The build stays green only if the rerun passed.
3. **Track.** Open a ticket for every flaky candidate. Tag the scenario `@flaky` while it is being fixed.
4. **Quarantine, don't delete.** Run `@flaky` in a separate non-blocking job (`TAGS="@flaky"` with `allow_failure`/`continue-on-error`). Exclude it from the gate (`TAGS="not @flaky"`).
5. **Never** raise retries above 1 or add `sleep` to make a pipeline green. Fix the wait strategy in the page object instead.

## Anti-patterns

| Don't | Do |
|-------|----|
| Duplicate the `behave …` command in every CI file | Call `run_tests.sh` |
| `playwright install` (all browsers) in every job | Install only `$BROWSER` and cache it |
| `continue-on-error: true` on the test step | Let it fail; collect artifacts with `if: always()` |
| `retry: 3` on the whole job | Rerun only failed scenarios, once, and report them |
| `HEADLESS=false` or `SLOW_MO>0` in CI | Headless, no slow-mo |
| Publish reports from PR branches to Pages | Publish from `main` only; upload PR reports as artifacts |
| `-t @smoke` on untagged features | Tag first, and keep the zero-test guard |
| `permissions: write-all` | Least privilege per job |
| `actions/checkout@master` / `image: latest` | Pinned versions |
| Hardcoded `sleep` to stabilise CI | Explicit waits in page objects |
