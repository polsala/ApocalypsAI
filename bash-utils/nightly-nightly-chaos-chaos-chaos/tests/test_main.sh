#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: We mock systemctl, tc, stress to avoid requiring root or network privileges.
mock_setup() {
  export PATH="$(pwd)/tests/mocks:$PATH"
}

# Run tests
main() {
  mock_setup
  ./src/main.sh --dry-run
  echo "Test passed: dry-run completed without errors."
}

main "$@"
