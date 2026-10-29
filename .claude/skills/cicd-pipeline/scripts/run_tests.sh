#!/usr/bin/env bash
# Single CI entrypoint for the Behave + Playwright suite.
# Every pipeline (GitHub Actions, GitLab, Jenkins) calls this script so that
# local runs and CI runs behave identically.
#
# Environment inputs (all optional):
#   BROWSER        chromium | firefox | webkit           (default: chromium)
#   TAGS           behave tag expression, e.g. "@smoke and not @wip" (default: all)
#   FEATURES       feature path(s) to run                (default: features)
#   RERUN_FAILED   1 = re-run failed scenarios once to detect flakiness (default: 1)
#   RESULTS_DIR    output root                           (default: results)
#
# Exit code: 0 when every scenario passes (on first run or on rerun), 1 otherwise.
#
# NOTE: behave.ini must not set `formatter`/`outfiles` - behave merges them with
# the -f/-o flags below and pairs formatters with the wrong output files.
set -uo pipefail

BROWSER="${BROWSER:-chromium}"
TAGS="${TAGS:-}"
FEATURES="${FEATURES:-features}"
RERUN_FAILED="${RERUN_FAILED:-1}"
RESULTS_DIR="${RESULTS_DIR:-results}"

export BROWSER
export HEADLESS="${HEADLESS:-true}"

ALLURE_DIR="${RESULTS_DIR}/allure-results"
JUNIT_DIR="${RESULTS_DIR}/junit"
RERUN_FILE="${RESULTS_DIR}/rerun.txt"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "${ALLURE_DIR}" "${JUNIT_DIR}" "${RESULTS_DIR}/screenshots" "${RESULTS_DIR}/logs"
rm -f "${RERUN_FILE}"

TAG_ARGS=()
if [[ -n "${TAGS}" ]]; then
  TAG_ARGS=(--tags "${TAGS}")
fi

# Formatters are passed explicitly so CI output does not depend on behave.ini.
FORMAT_ARGS=(
  --no-capture
  -f allure_behave.formatter:AllureFormatter -o "${ALLURE_DIR}"
  -f rerun -o "${RERUN_FILE}"
  -f progress
  --junit --junit-directory "${JUNIT_DIR}"
)

python -m behave "${FEATURES}" "${TAG_ARGS[@]}" "${FORMAT_ARGS[@]}"
STATUS=$?

if [[ ${STATUS} -ne 0 && "${RERUN_FAILED}" == "1" && -s "${RERUN_FILE}" ]]; then
  echo "First run failed - re-running failed scenarios once to separate flaky from broken:"
  cat "${RERUN_FILE}"
  cp "${RERUN_FILE}" "${RESULTS_DIR}/flaky-candidates.txt"
  # Rerun results land in the same Allure dir; Allure shows them as retries.
  python -m behave "@${RERUN_FILE}" "${FORMAT_ARGS[@]}"
  STATUS=$?
  if [[ ${STATUS} -eq 0 ]]; then
    echo "WARNING: failures passed on rerun - flaky scenarios listed in ${RESULTS_DIR}/flaky-candidates.txt"
  else
    # Still failing after rerun = genuinely broken, not flaky.
    rm -f "${RESULTS_DIR}/flaky-candidates.txt"
  fi
fi

# Label results with the browser so a merged cross-browser report keeps them apart.
python "${SCRIPT_DIR}/label_allure_results.py" "${ALLURE_DIR}" "${BROWSER}"

exit ${STATUS}
