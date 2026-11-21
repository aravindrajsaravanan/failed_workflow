
import os
import re
import json
import requests

OWNER = "aravindrajsaravanan"
REPO = "failed_workflow"
BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"

token = os.environ["GITHUB_TOKEN"]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}


def get_json(url):
    response = requests.get(
        url, headers=headers, timeout=30
    )
    response.raise_for_status()
    return response.json()


def analyze_failure(logs):
    # Remove ANSI color codes from logs
    clean_logs = re.sub(
        r"\x1b\[[0-9;]*m", "", logs
    )
    lower_logs = clean_logs.lower()

    if (
        "test_subtract" in lower_logs
        and "assert 14 == 6" in lower_logs
    ):
        return {
            "error_type": "AssertionError",
            "failed_test": "test_subtract",
            "root_cause": (
                "Known calculator bug: subtraction "
                "function performs addition."
            ),
            "suggested_fix": "return a - b",
            "analysis_type": "rule-based"
        }

    if "modulenotfounderror" in lower_logs:
        return {
            "error_type": "ModuleNotFoundError",
            "root_cause": (
                "A required Python module is missing "
                "from the execution environment."
            ),
            "suggested_fix": (
                "Check dependency installation, "
                "requirements.txt and Python environment."
            ),
            "analysis_type": "rule-based"
        }

    if "connection refused" in lower_logs:
        return {
            "error_type": "ConnectionError",
            "root_cause": (
                "The target service refused a "
                "network connection."
            ),
            "suggested_fix": (
                "Check service status, target host, "
                "port and network configuration."
            ),
            "analysis_type": "rule-based"
        }

    if "permission denied" in lower_logs:
        return {
            "error_type": "PermissionError",
            "root_cause": (
                "The process was denied access "
                "to a required resource."
            ),
            "suggested_fix": (
                "Check file permissions, credentials "
                "and access policies."
            ),
            "analysis_type": "rule-based"
        }

    if (
        "timeouterror" in lower_logs
        or "timed out" in lower_logs
    ):
        return {
            "error_type": "TimeoutError",
            "root_cause": (
                "An operation exceeded its allowed "
                "time limit."
            ),
            "suggested_fix": (
                "Check service availability, network "
                "latency and timeout configuration."
            ),
            "analysis_type": "rule-based"
        }

    if "assertionerror" in lower_logs:
        return {
            "error_type": "AssertionError",
            "root_cause": (
                "A test assertion failed; the exact "
                "cause requires investigation."
            ),
            "suggested_fix": (
                "Compare actual and expected results, "
                "then inspect the relevant code."
            ),
            "analysis_type": "rule-based"
        }

    return {
        "error_type": "Unknown",
        "root_cause": "Not determined",
        "suggested_fix": (
            "Review the failed step and its logs."
        ),
        "analysis_type": "rule-based"
    }


print("Checking failed GitHub Actions pipelines...")

runs = get_json(
    f"{BASE}/actions/runs?status=failure&per_page=30"
)["workflow_runs"]

calculator_runs = [
    run for run in runs
    if run["name"] == "Python Calculator Tests"
]

if not calculator_runs:
    print("No failed calculator runs found.")

else:
    run = calculator_runs[0]

    jobs = get_json(
        f"{BASE}/actions/runs/{run['id']}/jobs"
    )["jobs"]

    for job in jobs:
        if job["conclusion"] != "failure":
            continue

        response = requests.get(
            f"{BASE}/actions/jobs/{job['id']}/logs",
            headers=headers,
            timeout=60
        )
        response.raise_for_status()

        analysis = analyze_failure(response.text)

        report = {
            "repository": f"{OWNER}/{REPO}",
            "workflow": run["name"],
            "run_id": run["id"],
            "run_url": run["html_url"],
            "job": job["name"],
            "conclusion": job["conclusion"],
            "analysis": analysis
        }

        with open(
            "failure_report.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(report, file, indent=4)

        print("===== FAILURE REPORT =====")
        print(json.dumps(report, indent=4))
        print("Report saved: failure_report.json")
        break
