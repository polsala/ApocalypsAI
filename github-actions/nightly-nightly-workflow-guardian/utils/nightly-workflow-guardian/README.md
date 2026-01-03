# Nightly Workflow Guardian

This utility acts as a vigilant sentinel for your GitHub Actions workflows. It periodically checks the status of recent workflow runs across your repository and reports any anomalies or failures, ensuring your automation pipeline remains robust and reliable.

## Purpose

To provide an automated, nightly check of GitHub Actions workflow health, alerting maintainers to potential issues before they escalate.

## How it Works

The guardian script queries the GitHub API to fetch recent workflow runs. It analyzes their status (success, failure, cancelled, etc.) and identifies any patterns of concern, such as a high rate of failures or a critical workflow failing.

## Usage

This utility is designed to be run as a GitHub Actions workflow itself. The `.github/workflows/nightly-workflow-guardian.yml` file defines this workflow.

It requires the `GITHUB_TOKEN` to authenticate with the GitHub API.

## Configuration

Currently, the guardian is configured to check all workflows in the repository. Future enhancements might include configurable thresholds or specific workflow monitoring.

## Output

- If all workflows are healthy, the action will complete successfully with no visible output beyond standard logs.
- If issues are detected (e.g., a workflow failed), the action will output a failure status and create a GitHub Issue to notify maintainers.
