#!/bin/bash

# This script generates a workflow wellness report based on GitHub Actions run data.
# It identifies long-running and frequently failing workflows.

# Inputs (passed as arguments from action.yml)
REPO=$1
MAX_RUNS=$2
LONG_RUN_THRESHOLD_MINUTES=$3
FAILURE_FREQUENCY_THRESHOLD=$4

# GH_TOKEN is expected to be in the environment, set by the action.yml
if [[ -z "$GH_TOKEN" ]]; then
    echo "Error: GH_TOKEN environment variable is not set. Please provide a GitHub token." >&2
    exit 1
fi

# Fetch workflow runs using GitHub CLI (gh)
# Mock rationale: In a real scenario, this would call `gh run list`. For testing, a mock `gh` command is used.
RUNS_JSON=$(gh run list --repo "$REPO" --limit "$MAX_RUNS" --json databaseId,name,status,conclusion,createdAt,updatedAt,url)

REPORT_SUMMARY="### Workflow Wellness Report\n\n"
LONG_RUN_REPORT=""
FAILURE_REPORT=""

# --- Long Running Workflows ---
# Use jq to filter and format long-running workflows
LONG_RUN_DATA=$(echo "$RUNS_JSON" | jq -r --argjson threshold_minutes "$LONG_RUN_THRESHOLD_MINUTES" '
  .[] |
  # Only consider completed runs (success or failure) for duration calculation
  select(.status == "completed" and (.conclusion == "success" or .conclusion == "failure")) |
  {
    name: .name,
    url: .url,
    # Convert ISO 8601 strings to Unix timestamps for calculation
    createdAt: (.createdAt | fromdateiso8601),
    updatedAt: (.updatedAt | fromdateiso8601)
  } |
  # Calculate duration in minutes and filter if it exceeds the threshold
  select(((.updatedAt - .createdAt) / 60) > $threshold_minutes) |
  "  - Workflow: \(.name), Duration: \(((.updatedAt - .createdAt) / 60) | round)m, URL: \(.url)"
')

if [[ -n "$LONG_RUN_DATA" ]]; then
    LONG_RUN_REPORT="#### Long-Running Workflows (>${LONG_RUN_THRESHOLD_MINUTES} minutes):\n${LONG_RUN_DATA}\n\n"
else
    LONG_RUN_REPORT="#### Long-Running Workflows (>${LONG_RUN_THRESHOLD_MINUTES} minutes):\n  _No long-running workflows detected._\n\n"
fi

# --- Frequently Failing Workflows ---
# Group runs by workflow name and count failures for each
FAILURE_COUNTS=$(echo "$RUNS_JSON" | jq -r '
  map(select(.conclusion == "failure")) |
  group_by(.name) |
  map({
    name: .[0].name,
    failures: length,
    last_failure_url: .[0].url # Get URL of the most recent failure for context
  }) |
  .[] | "\(.name)|\(.failures)|\(.last_failure_url)"
')

declare -A workflow_failure_map # Associative array to store failure counts and URLs
while IFS='|' read -r name failures url; do
    workflow_failure_map["$name"]="$failures|$url"
done <<< "$FAILURE_COUNTS"

FREQUENT_FAILURE_DETAILS=""
for workflow_name in "${!workflow_failure_map[@]}"; do
    IFS='|' read -r failures url <<< "${workflow_failure_map["$workflow_name"]}"
    if [[ "$failures" -ge "$FAILURE_FREQUENCY_THRESHOLD" ]]; then
        FREQUENT_FAILURE_DETAILS+="  - Workflow: $workflow_name, Failures in last ${MAX_RUNS} runs: ${failures}, Last Failure URL: $url\n"
    fi
done

if [[ -n "$FREQUENT_FAILURE_DETAILS" ]]; then
    FAILURE_REPORT="#### Frequently Failing Workflows (>= ${FAILURE_FREQUENCY_THRESHOLD} failures in last ${MAX_RUNS} runs):\n${FREQUENT_FAILURE_DETAILS}"
else
    FAILURE_REPORT="#### Frequently Failing Workflows (>= ${FAILURE_FREQUENCY_THRESHOLD} failures in last ${MAX_RUNS} runs):\n  _No frequently failing workflows detected._\n"
fi

REPORT_SUMMARY+="$LONG_RUN_REPORT"
REPORT_SUMMARY+="$FAILURE_REPORT"

# Set the output for the GitHub Action
echo "::set-output name=report-summary::$REPORT_SUMMARY"

# Also print to stdout for immediate visibility in logs
echo "$REPORT_SUMMARY"
