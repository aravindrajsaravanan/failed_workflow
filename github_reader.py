
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
        print("Downloading job logs...")

        log_url = f"{BASE}/actions/jobs/{job['id']}/logs"
        response = requests.get(
            log_url, headers=headers, timeout=60
        )
        response.raise_for_status()

        log_lines = response.text.splitlines()

        print("Relevant error lines:")
        for line in log_lines:
            if any(word in line.lower() for word in [
                "assertionerror",
                "assert 14 == 6",
                "test_subtract",
                "failed"
            ]):
                print(line[:500])
