#!/bin/bash
# mock_date.sh
# Mock rationale: This script replaces the standard 'date' command during testing
# to provide deterministic timestamps for the "current time", ensuring that
# date-based calculations within the action are consistent across test runs.
# It allows the action to calculate age relative to a fixed "now".

# Check if MOCKED_CURRENT_TIMESTAMP is set, otherwise fall back to real date
if [[ -z "${MOCKED_CURRENT_TIMESTAMP}" ]]; then
  /bin/date "$@"
  exit $?
fi

if [[ "$1" == "+%s" ]]; then
  echo "${MOCKED_CURRENT_TIMESTAMP}"
elif [[ "$1" == "-d" ]]; then
  # For parsing specific dates from the PR JSON, use the real date command.
  # These dates are fixed in the mock JSON, so their parsing doesn't need mocking.
  /bin/date "$@"
else
  # Fallback for any other date command usage
  /bin/date "$@"
fi
