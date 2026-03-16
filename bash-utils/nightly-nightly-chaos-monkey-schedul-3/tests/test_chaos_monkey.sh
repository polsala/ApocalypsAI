#!/bin/bash

# Mock rationale: We avoid actual system changes during testing by overriding disruptive functions.

CHAOS_MONKEY_SCRIPT="../src/chaos_monkey.sh"
MOCK_OUTPUT_FILE="/tmp/chaos_mock_output.txt"

setup() {
  unset CHAOS_PID_FILE INTERVAL DRY_RUN ACTION
  export CHAOS_PID_FILE="/tmp/test_chaos.pid"
  touch "$MOCK_OUTPUT_FILE"
}

teardown() {
  rm -f "$MOCK_OUTPUT_FILE" "$CHAOS_PID_FILE"
}

mock_disrupt_functions() {
  disrupt_service() { echo "[MOCK] Service disrupted" >> "$MOCK_OUTPUT_FILE"; }
  disrupt_network() { echo "[MOCK] Network disrupted" >> "$MOCK_OUTPUT_FILE"; }
  disrupt_disk_io() { echo "[MOCK] Disk I/O disrupted" >> "$MOCK_OUTPUT_FILE"; }
}

source_and_mock() {
  source "$CHAOS_MONKEY_SCRIPT"
  mock_disrupt_functions
}

test_start_stop() {
  setup
  source_and_mock
  start_chaos &
  sleep 1
  assert_file_contains "$MOCK_OUTPUT_FILE" "[MOCK]"
  stop_chaos
  teardown
}

test_dry_run_mode() {
  setup
  source_and_mock
  DRY_RUN=true
  disrupt_service
  assert_file_contains "$MOCK_OUTPUT_FILE" "[DRY RUN] Would restart service"
  teardown
}

test_parse_interval_seconds() {
  setup
  source_and_mock
  parse_args "--interval=5s"
  [[ "$INTERVAL" == "5s" ]] || fail "Expected interval 5s, got $INTERVAL"
  teardown
}

test_parse_interval_minutes() {
  setup
  source_and_mock
  parse_args "--interval=2m"
  [[ "$INTERVAL" == "2m" ]] || fail "Expected interval 2m, got $INTERVAL"
  teardown
}

assert_file_contains() {
  local file=$1
  local pattern=$2
  grep -q "$pattern" "$file" || fail "File $file does not contain '$pattern'"
}

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

run_tests() {
  test_parse_interval_seconds
  test_parse_interval_minutes
  test_dry_run_mode
  test_start_stop
  echo "All tests passed."
}

run_tests
