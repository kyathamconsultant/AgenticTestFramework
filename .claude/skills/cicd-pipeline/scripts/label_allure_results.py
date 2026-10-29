"""
Tag Allure result files with the browser they ran on.

Without this, the same scenario run on chromium/firefox/webkit shares one
historyId, and a merged Allure report shows them as retries of a single test.
Adding a "browser" parameter and folding it into historyId/testCaseId makes
each browser a distinct test, which is how Allure models parametrized runs.

Usage: python label_allure_results.py <allure-results-dir> <browser>
"""
import hashlib
import json
import platform
import sys
from pathlib import Path


def _rehash(value, browser):
    return hashlib.md5(f"{value}:{browser}".encode("utf-8")).hexdigest()


def label_results(results_dir, browser):
    labelled = 0
    for result_file in results_dir.glob("*-result.json"):
        data = json.loads(result_file.read_text(encoding="utf-8"))
        params = data.setdefault("parameters", [])
        if any(p.get("name") == "browser" for p in params):
            continue
        params.append({"name": "browser", "value": browser})
        for key in ("historyId", "testCaseId"):
            if key in data:
                data[key] = _rehash(data[key], browser)
        data["name"] = f"{data.get('name', '')} [{browser}]"
        result_file.write_text(json.dumps(data), encoding="utf-8")
        labelled += 1
    return labelled


def write_environment(results_dir, browser):
    env_file = results_dir / "environment.properties"
    lines = {}
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                lines[key] = value
    browsers = set(filter(None, lines.get("Browsers", "").split(",")))
    browsers.add(browser)
    lines["Browsers"] = ",".join(sorted(browsers))
    lines["Python"] = platform.python_version()
    lines["OS"] = platform.platform()
    env_file.write_text("\n".join(f"{k}={v}" for k, v in lines.items()) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python label_allure_results.py <allure-results-dir> <browser>")
    target = Path(sys.argv[1])
    if not target.is_dir():
        print(f"No Allure results at {target}; nothing to label")
        sys.exit(0)
    count = label_results(target, sys.argv[2])
    write_environment(target, sys.argv[2])
    print(f"Labelled {count} Allure result(s) with browser={sys.argv[2]}")
