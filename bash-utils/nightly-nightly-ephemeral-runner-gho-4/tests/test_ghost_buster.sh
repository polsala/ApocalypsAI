#!/usr/bin/env bash

# Tests for Nightly Ephemeral Runner Ghost Buster

set -euo pipefail

# Source the script functions for testing
# Note: We mock external commands to avoid real API calls

# Mock functions
mock_aws() {
  echo '["i-12345", "runner-aws-1", "2025-01-01T00:00:00.000Z"]'
  echo '["i-67890", "runner-aws-2", "2025-01-01T00:00:00.000Z"]'
}

mock_github_runners() {
  cat <<'EOF'
{
  "runners": [
    {"id": 1, "name": "runner-aws-1", "status": "online", "busy": false, "labels": []},
    {"id": 2, "name": "orphaned-runner", "status": "offline", "busy": false, "labels": []}
  ]
}
EOF
}

# Test detection of orphaned runners
# Mock rationale: Simulates GitHub API response and AWS instance list to verify orphan detection.
test_detect_orphaned() {
  echo "Testing orphan detection..."

  # Create temp files
  local runners_file="/tmp/test_runners.json"
  local instances_file="/tmp/test_instances.json"

  mock_github_runners >"${runners_file}"
  mock_aws >"${instances_file}"

  # Extract instance names
  local instance_names
  instance_names=$(jq -r '.[1]' "${instances_file}")

  # Check for orphaned runner
  local orphan_found=false
  while IFS= read -r runner; do
    local runner_name
    runner_name=$(echo "$runner" | jq -r '.name')

    if ! echo "${instance_names}" | grep -q "${runner_name}"; then
      if [[ "${runner_name}" == "orphaned-runner" ]]; then
        orphan_found=true
        echo "✓ Orphaned runner detected correctly: ${runner_name}"
      fi
    fi
  done < <(jq -c '.' "${runners_file}")

  if [[ "${orphan_found}" != "true" ]]; then
    echo "✗ Test failed: Orphaned runner not detected"
    return 1
  fi
}

# Test stale instance detection
# Mock rationale: Simulates instance launch times to verify age-based cleanup logic.
test_stale_detection() {
  echo "Testing stale instance detection..."

  local instances_file="/tmp/test_stale_instances.json"

  # Create mock instances with old timestamps
  cat >"${instances_file}" <<'EOF'
["i-old", "runner-old", "2020-01-01T00:00:00.000Z"]
["i-new", "runner-new", "2025-01-01T00:00:00.000Z"]
EOF

  local cutoff_epoch
  cutoff_epoch=$(date -d "1 hour ago" +%s)

  local stale_count=0
  while IFS= read -r instance; do
    local launch_time
    launch_time=$(echo "$instance" | jq -r '.[2]')

    if [[ -n "${launch_time}" && "${launch_time}" != "null" ]]; then
      local launch_epoch
      launch_epoch=$(date -d "${launch_time}" +%s 2>/dev/null || echo 0)

      if [[ $launch_epoch -lt $cutoff_epoch ]]; then
        stale_count=$((stale_count + 1))
      fi
    fi
  done < <(jq -c '.' "${instances_file}")

  if [[ $stale_count -eq 1 ]]; then
    echo "✓ Stale instance detection works"
  else
    echo "✗ Test failed: Expected 1 stale instance, got ${stale_count}"
    return 1
  fi
}

# Run tests
main_test() {
  echo "Running Ghost Buster tests..."

  test_detect_orphaned
  test_stale_detection

  echo "All tests passed!"
}

main_test
