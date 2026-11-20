
import requests

OWNER = "aravindrajsaravanan"
REPO = "failed_workflow"

url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"

response = requests.get(url, timeout=15)
response.raise_for_status()

runs = response.json().get("workflow_runs", [])

for run in runs[:5]:
    print("Run ID:", run["id"])
    print("Status:", run["status"])
    print("Conclusion:", run["conclusion"])
    print("URL:", run["html_url"])
    print("--------------------")
