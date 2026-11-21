
import os
import json
import requests

OWNER = "aravindrajsaravanan"
REPO = "failed_workflow"
BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"

token = os.environ["GITHUB_TOKEN"]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
}

def get_json(url):
    response = requests.get(
        url, headers=headers, timeout=30
    )
    response.raise_for_status()
    return response.json()

def analyze_failure(logs):
    if "test_subtract" in logs and "assert 14 == 6" in logs:
        return {
            "failed_test": "test_subtract",
            "error": "AssertionError: assert 14 == 6",
            "actual_result": 14,
            "expected_result": 6,
            "root_cause": (
                "Incorrect subtraction logic. "
                "The function adds instead of subtracting."
            ),
            "suggested_fix": "return a - b",
            "analysis_type": "rule-based"
        }

    return {
        "failed_test": "unknown",
        "error": "Unrecognized failure",
        "root_cause": "Further investigation required",
        "suggested_fix": "Manual or AI analysis required",
        "analysis_type": "rule-based"
    }

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

        logs = response.text
        analysis = analyze_failure(logs)

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
            "failure_report.json", "w", encoding="utf-8"
        ) as file:
            json.dump(report, file, indent=4)

        print("===== FAILURE REPORT =====")
        print(json.dumps(report, indent=4))
        print("Report saved: failure_report.json")
        break
