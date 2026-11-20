
import requests

OWNER = "aravindrajsaravanan"
REPO = "failed_workflow"

url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"

response = requests.get(url, timeout=15)
response.raise_for_status()

runs = response.json().get("workflow_runs", [])

print("Checking GitHub Actions for failed pipelines...")

failed_runs = [
    run for run in runs
    if run["conclusion"] == "failure"
]

if not failed_runs:
    print("No failed pipelines found in recent runs.")
else:
    for run in failed_runs:
        print("--------------------")
        print("Workflow:", run["name"])
        print("Run ID:", run["id"])
        print("Conclusion:", run["conclusion"])
        print("URL:", run["html_url"])

print("Total failed runs found:", len(failed_runs))
