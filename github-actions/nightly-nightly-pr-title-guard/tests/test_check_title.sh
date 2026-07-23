#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
CHECK_SCRIPT="${SCRIPT_DIR}/check_title.sh"

# Helper to run a test case
run_test() {
  local name="$1"
  local json_content="$2"
  local min_len="$3"
  local expect_success="$4"

  tmpfile=$(mktemp)
  echo "${json_content}" > "${tmpfile}"
  export GITHUB_EVENT_PATH="${tmpfile}"

  if "${CHECK_SCRIPT}" "${min_len}"; then
    result=0
  else
    result=1
  fi

  if [[ "${result}" -eq 0 && "${expect_success}" == "true" ]] || [[ "${result}" -ne 0 && "${expect_success}" == "false" ]]; then
    echo "PASS: ${name}"
  else
    echo "FAIL: ${name}"
    exit 1
  fi

  rm -f "${tmpfile}"
}

# Test 1: sufficient length
run_test "sufficient-length" '{"pull_request":{"title":"Add comprehensive documentation for the new API"}}' 10 true

# Test 2: too short
run_test "too-short" '{"pull_request":{"title":"Fix"}}' 10 false

echo "All tests passed."
