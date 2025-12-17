## Nightly Workflow Watcher

This GitHub Actions workflow is designed to keep a vigilant eye on your repository's other GitHub Actions workflows. It periodically checks for runs that have failed unexpectedly or have been running for an unusually long time, providing timely alerts to prevent potential issues from going unnoticed.

### How it Works

The workflow triggers on a schedule (e.g., daily) and uses the GitHub API to query recent workflow runs for the repository. It then applies configurable thresholds to identify problematic runs.

### Configuration

- `FAILURE_THRESHOLD`: The maximum number of recent failed runs to consider before triggering an alert. Defaults to 1.
- `LONG_RUN_THRESHOLD_MINUTES`: The maximum duration (in minutes) a workflow run can take before being flagged as potentially too long. Defaults to 60.
- `REPO_OWNER`: The owner of the repository (e.g., 'polsala').
- `REPO_NAME`: The name of the repository (e.g., 'ApocalypsAI').

### Usage

1.  Add this workflow file (`.github/workflows/nightly-workflow-watcher.yml`) to your repository.
2.  Configure the `env` variables in the workflow file to match your repository's details and desired thresholds.
3.  The workflow will automatically run on its defined schedule.

### Example Alert Message

If a workflow run fails or takes too long, a comment will be posted on the workflow run's page (if accessible) or an issue might be created (depending on future enhancements).

```
🚨 Workflow Alert!

Workflow "Build and Deploy" (run ID: 123456789) failed unexpectedly.

Check details: https://github.com/polsala/ApocalypsAI/actions/runs/123456789
```

```
⏳ Workflow Alert!

Workflow "Integration Tests" (run ID: 987654321) has been running for over 70 minutes, exceeding the threshold of 60 minutes.

Check details: https://github.com/polsala/ApocalypsAI/actions/runs/987654321
```
