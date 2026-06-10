#!/usr/bin/env bash
# test_label_pr.sh – deterministic tests for label_pr.sh

set -euo pipefail

# Load the script under test
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)
source "$SCRIPT_DIR/label_pr.sh"

# Helper to capture output
run_test() {
  local input="$1"
  local expected="$2"
  local output
  output=$(bash "$SCRIPT_DIR/label_pr.sh" "$input" 2>/dev/null | grep '^::set-output' || true)
  # Extract the value after the last ::
  local actual=$(echo "$output" | awk -F'::' '{print $NF}')
  if [[ "$actual" == "$expected" ]]; then
    echo "PASS: input='$input' => '$actual'"
  else
    echo "FAIL: input='$input' => expected '$expected' but got '$actual'"
    exit 1
  fi
}

# Mock rationale: Using static inputs ensures deterministic behavior without external GitHub context.

# Test 1 – docs only
run_test "README.md,CONTRIBUTING.txt" "📚 docs-only"

# Test 2 – test files only
run_test "module_test.py,utils_spec.js" "🧪 test-only"

# Test 3 – config change + code change
run_test ".github/workflows/ci.yml,src/main.py" "⚙️ config-change,🚀 code-change"

# Test 4 – mixed docs and code (should get both docs and code labels)
run_test "README.md,src/app.js" "📚 docs-only,🚀 code-change"

# Test 5 – no recognizable patterns (fallback label)
run_test "random.bin,unknown.xyz" "🔧 miscellaneous-change"

echo "All tests passed."
