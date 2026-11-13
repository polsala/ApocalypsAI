#!/bin/bash

MAX_STALE_HOURS=${1:-24}
FAIL_ON_STALE=${2:-false}
FAIL_ON_FUTURE=${3:-true}

echo "--- Nightly Chrono-Sync Check ---"
echo "Max stale hours: $MAX_STALE_HOURS"
echo "Fail on stale: $FAIL_ON_STALE"
echo "Fail on future: $FAIL_ON_FUTURE"

# Get current time in UTC seconds since epoch
# Mock rationale: In a real GitHub Action, $EPOCH_SECONDS would be `date +%s`. For testing,
# we'll inject a specific value via environment variable.
WORKFLOW_RUN_EPOCH=${EPOCH_SECONDS:-$(date +%s)}
echo "Workflow run time (epoch): $WORKFLOW_RUN_EPOCH"

# Get latest commit time in UTC seconds since epoch
# Mock rationale: In a real GitHub Action, this would be `git log -1 --format=%at`. For testing,
# we'll inject a specific value via environment variable.
LATEST_COMMIT_EPOCH=${MOCKED_COMMIT_EPOCH:-$(git log -1 --format=%at)}
echo "Latest commit time (epoch): $LATEST_COMMIT_EPOCH"

# Calculate time difference in seconds
TIME_DIFF_SECONDS=$((WORKFLOW_RUN_EPOCH - LATEST_COMMIT_EPOCH))
TIME_DIFF_HOURS=$(echo "scale=2; $TIME_DIFF_SECONDS / 3600" | bc)

echo "Time difference: $TIME_DIFF_SECONDS seconds ($TIME_DIFF_HOURS hours)"

IS_STALE="false"
IS_FUTURE="false"
EXIT_CODE=0

# Check for future commit
if (( TIME_DIFF_SECONDS < 0 )); then
  echo "🚨 Temporal Anomaly Detected! Latest commit is in the future by $(( -TIME_DIFF_SECONDS )) seconds!"
  IS_FUTURE="true"
  if [[ "$FAIL_ON_FUTURE" == "true" ]]; then
    echo "::error::Commit timestamp is in the future. Failing workflow as configured."
    EXIT_CODE=1
  fi
fi

# Check for stale commit
# Use floating point comparison for hours
if (( $(echo "$TIME_DIFF_HOURS > $MAX_STALE_HOURS" | bc -l) )); then
  echo "⏳ Latest commit is stale! It's $TIME_DIFF_HOURS hours old, exceeding $MAX_STALE_HOURS hours."
  IS_STALE="true"
  if [[ "$FAIL_ON_STALE" == "true" ]]; then
    echo "::error::Commit timestamp is too old. Failing workflow as configured."
    EXIT_CODE=1
  fi
fi

echo "::set-output name=is-stale::$IS_STALE"
echo "::set-output name=is-future::$IS_FUTURE"
echo "::set-output name=time-difference-hours::$TIME_DIFF_HOURS"

exit $EXIT_CODE
