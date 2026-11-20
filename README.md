# Failed Workflow — DevOps AI Agent Practice Lab

This repository is a safe practice environment for investigating failed GitHub Actions pipelines.

## Stage 1: Intentionally failing calculator test

The Python calculator contains a **deliberate subtraction bug**. Do not fix it yet: the failure is the test case for a future AI DevOps agent that will inspect GitHub Actions logs, diagnose causes, and recommend safe changes.

### Run locally

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

Expected outcome for this stage: **one failing subtraction test** and other passing tests.

### GitHub Actions

Open the **Actions** tab and select **Python Calculator Tests** to view the failed run and its logs.

No AI agent or automatic fixes are installed in this stage.
