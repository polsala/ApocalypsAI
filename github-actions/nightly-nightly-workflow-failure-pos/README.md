Nightly Workflow Failure Postmortem

A GitHub Action that automatically creates an issue when a workflow run fails. It records the workflow name, run URL, run ID and timestamp.

Usage:

In a workflow, add a job that runs on workflow_run events with conclusion failure, and use this action with the required input github-token.

Inputs:

github-token (required) â token with repo scope.

How it works:

The action runs a Bash script that calls the GitHub REST API to create an issue titled "Workflow Failure: <workflow name>" with a body containing details.
