#!/usr/bin/env bash
# Tests for nightly-emoji-enhancer
# ---------------------------------------------------------------
# Helper for assertions
assert_eq() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "[PASS] $test_name"
    else
        echo "[FAIL] $test_name"
        echo "  Expected: $expected"
        echo "  Got     : $actual"
        exit 1
    fi
}

# Path to the script under test
SCRIPT="$(dirname "${BASH_SOURCE[0]}")/../src/emoji_enhance.sh"

# Test 1: keyword "fix"
output=$(bash "$SCRIPT" "Fix critical bug in login")
assert_eq "🛠️ Fix critical bug in login" "$output" "detects 'fix' keyword"

# Test 2: keyword "add"
output=$(bash "$SCRIPT" "Add new endpoint for metrics")
assert_eq "➕ Add new endpoint for metrics" "$output" "detects 'add' keyword"

# Test 3: keyword "remove"
output=$(bash "$SCRIPT" "Remove deprecated flag")
assert_eq "➖ Remove deprecated flag" "$output" "detects 'remove' keyword"

# Test 4: keyword "update"
output=$(bash "$SCRIPT" "Update README with usage examples")
assert_eq "🔄 Update README with usage examples" "$output" "detects 'update' keyword"

# Test 5: no matching keyword – default emoji
output=$(bash "$SCRIPT" "Celebrate successful deployment")
assert_eq "🎉 Celebrate successful deployment" "$output" "uses default emoji when no keyword matches"

# Test 6: reading from STDIN
output=$(echo "Add feature X" | bash "$SCRIPT")
assert_eq "➕ Add feature X" "$output" "reads from STDIN correctly"

# All tests passed
exit 0
