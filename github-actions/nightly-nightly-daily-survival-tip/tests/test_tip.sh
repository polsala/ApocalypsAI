#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Override curl to capture request without network
captured_url=""
captured_data=""

curl() {
  captured_url="$1"
  shift
  while (( "$#" )); do
    case "$1" in
      -d)
        captured_data="$2"
        shift 2
        ;;
      *)
        shift
        ;;
    esac
  done
  echo "mock curl called"
}
export -f curl

# Mock rationale: Override date to return a fixed day of year (005)
date() {
  if [[ "$*" == "+%j" ]]; then
    echo "005"
  else
    command date "$@"
  fi
}
export -f date

# Set required environment variables
export GITHUB_REPOSITORY="owner/repo"
export INPUT_GITHUB_TOKEN="fake-token"

# Run the tip script
bash src/tip.sh

# Expected tip for day 5 (index 4) is "Map your surroundings daily"
expected_body="Map your surroundings daily"
if [[ "$captured_data" != *"$expected_body"* ]]; then
  echo "Test failed: expected body $expected_body, got $captured_data"
  exit 1
fi
echo "Test passed"
