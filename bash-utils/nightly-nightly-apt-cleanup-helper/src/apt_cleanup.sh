#!/usr/bin/env bash

set -e

MODE="dry-run"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) MODE="dry-run"; shift ;;
    --execute) MODE="execute"; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Function to obtain apt‑get output (real or mocked)
get_apt_output() {
  if [[ -n "$MOCK_APT_GET_OUTPUT" ]]; then
    echo -e "$MOCK_APT_GET_OUTPUT"
  else
    # Real commands (may require sudo)
    apt-get -s autoremove
    apt-get clean -s
  fi
}

if [[ "$MODE" == "dry-run" ]]; then
  echo "=== Dry Run: Packages that would be autoremoved ==="
  get_apt_output
else
  echo "=== Executing apt-get autoremove ==="
  apt-get -y autoremove
  echo "=== Executing apt-get clean ==="
  apt-get clean
fi
