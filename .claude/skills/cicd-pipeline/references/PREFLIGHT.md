# Project Preflight Checklist

Check every item against the repo before writing a pipeline. A failing item will break the pipeline on a clean runner. Report blockers to the user and fix them only with their approval.

Status column = state found in this framework on 2026-10-29. Re-verify; it may have been fixed since.

| # | Check | How to verify | Status | Fix |
|---|-------|---------------|--------|-----|
| 1 | `pip install -r requirements.txt` works on a clean machine | `pip index versions <pkg>` for each unusual package | **Blocker.** `allure-commandline` is not a PyPI package | Remove that line. The Allure CLI is installed separately in the report job (Java tarball) |
| 2 | `behave.ini` does not hard-code `formatter`/`outfiles` | Read `behave.ini` | **Blocker.** Behave merges these with CLI `-f/-o`, so the formatter-to-outfile pairing breaks (`FileExistsError` on `results/allure-results/behave.json`). That JSON is also not Allure format | Delete the `formatter` and `outfiles` lines and pass formatters on the CLI (`run_tests.sh` does this) |
| 3 | Headless works in CI | `config/config.py` reads `HEADLESS` from env | OK. `.env` has `HEADLESS=false`, but `load_dotenv()` does not override existing env vars, so `HEADLESS=true` from CI wins | None |
| 4 | `.env` not committed; `.gitignore` exists | `git ls-files .env .gitignore` | `.env` is tracked and there is no `.gitignore` | Add a `.gitignore` (`.env`, `results/`, `__pycache__/`, `venv/`, `allure-report/`). Commit `.env.example` |
| 5 | Unset secrets don't become empty strings | `grep os.getenv config/config.py` | Risk. An empty CI secret overrides the default with `""` | Create the secret, or don't map it at all |
| 6 | Feature files are tagged for tag-based stages | `grep -n "@" features/*.feature` | No tags exist, so `-t @smoke` would select 0 scenarios | Tag scenarios (`@smoke`, `@regression`, `@critical`) before splitting stages. Until then, run the full suite |
| 7 | Python version | `python --version`; docs | Local 3.13; framework claims 3.8+ | Use 3.12 in CI. Optionally add the minimum version to the lint matrix |
| 8 | Runner works locally | `HEADLESS=true bash .claude/skills/cicd-pipeline/scripts/run_tests.sh` | Fails until #2 is fixed | Fix #2, then re-run |
