
import os
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
    print("\n===== ROOT CAUSE ANALYSIS =====")

    if "test_subtract" in logs and (
        "assert 14 == 6" in logs
        or "assert 14 == 6" in logs.replace("  ", " ")
    ):
        print("Failed test: test_subtract")
        print("Actual result: 14")
        print("Expected result: 6")
        print("Likely cause: Incorrect subtraction logic")
        print("Known issue: subtract() adds instead of subtracting")
        print("Suggested fix: return a - b")
    else:
        print("No matching rule found.")
        print("Manual or AI analysis required.")

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
    print("Failed workflow:", run["name"])
    print("Run ID:", run["id"])

    jobs = get_json(
        f"{BASE}/actions/runs/{run['id']}/jobs"
    )["jobs"]

    for job in jobs:
        if job["conclusion"] != "failure":
            continue

        print("Failed job:", job["name"])

        response = requests.get(
            f"{BASE}/actions/jobs/{job['id']}/logs",
            headers=headers,
            timeout=60
        )
        response.raise_for_status()

        logs = response.text

        print("\nRelevant error lines:")
        for line in logs.splitlines():
            if any(word in line.lower() for word in [
                "assertionerror",
                "assert 14 == 6",
                "test_subtract",
            ]):
                print(line[:500])

        analyze_failure(logs)
