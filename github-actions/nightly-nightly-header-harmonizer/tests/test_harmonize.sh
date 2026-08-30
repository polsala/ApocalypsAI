#!/bin/bash
set -euo pipefail

# Mock rationale: This test script directly invokes the `harmonize.sh` script
# and uses standard shell commands (`mkdir`, `echo`, `cat`, `rm`, `diff`)
# to create temporary files, run the script, and assert its behavior.
# All operations are local, deterministic, and do not rely on external services.

SCRIPT_DIR=$(dirname "$(realpath "$0")")
HARMONIZE_SCRIPT="$SCRIPT_DIR/../src/harmonize.sh"

# Create a temporary directory for tests
TEST_DIR=$(mktemp -d)
echo "Running tests in $TEST_DIR"
cd "$TEST_DIR"

# Ensure the script is executable
chmod +x "$HARMONIZE_SCRIPT"

# Define a common header content (without comment markers)
COMMON_HEADER_CONTENT="ApocalypsAI Header Harmonizer\nForged in the fires of the Nightly Integrator.\nEnsuring cosmic consistency, one file at a time.\n(c) 2024 ApocalypsAI. All rights reserved."

# Helper function to format header for a given file type (duplicates logic for testing independence)
format_header_for_file() {
    local file_extension="$1"
    local content="$2"
    local prefix=""
    local suffix=""

    case "$file_extension" in
        py|sh|yml|yaml|md|txt) prefix="#" ;;
        js|ts|jsx|tsx|go|java|c|cpp|h|hpp) prefix="//" ;;
        html|xml) prefix="<!--"; suffix="-->" ;;
        css) prefix="/*"; suffix="*/" ;;
        *) echo "Unknown extension: $file_extension" >&2; return 1 ;;
    esac

    local formatted_header=""
    IFS=$'\n' read -ra lines <<< "$content"
    for line in "${lines[@]}"; do
        if [[ -n "$suffix" ]]; then # Block comments
            formatted_header+="$prefix $line $suffix\n"
        else # Line comments
            formatted_header+="$prefix $line\n"
        fi
    done
    echo -e "$formatted_header"
}

# --- Test Case 1: File with correct header (no fix-mode) ---
echo "--- Test Case 1: Correct header, no fix ---"
CORRECT_PY_HEADER=$(format_header_for_file py "$COMMON_HEADER_CONTENT")
echo -e "$CORRECT_PY_HEADER\nprint('Hello, world!')" > correct.py
OUTPUT=$(GITHUB_OUTPUT=/dev/null "$HARMONIZE_SCRIPT" "$COMMON_HEADER_CONTENT" "*.py" "false" 2>&1 || true)
if echo "$OUTPUT" | grep -q "All matched files are compliant."; then
    echo "PASS: Test Case 1"
else
    echo "FAIL: Test Case 1 - Output: $OUTPUT"
    exit 1
fi

# --- Test Case 2: File with no header (no fix-mode) ---
echo "--- Test Case 2: No header, no fix ---"
echo "console.log('Hello, JS!');" > no_header.js
OUTPUT=$(GITHUB_OUTPUT=/dev/null "$HARMONIZE_SCRIPT" "$COMMON_HEADER_CONTENT" "*.js" "false" 2>&1 || true)
if echo "$OUTPUT" | grep -q "File no_header.js is missing or has an incorrect header." && \
   echo "$OUTPUT" | grep -q "The following files are non-compliant:"; then
    echo "PASS: Test Case 2"
else
    echo "FAIL: Test Case 2 - Output: $OUTPUT"
    exit 1
fi

# --- Test Case 3: File with incorrect header (no fix-mode) ---
echo "--- Test Case 3: Incorrect header, no fix ---"
echo "// Wrong header\nconsole.log('Hello, JS!');" > incorrect.js
OUTPUT=$(GITHUB_OUTPUT=/dev/null "$HARMONIZE_SCRIPT" "$COMMON_HEADER_CONTENT" "*.js" "false" 2>&1 || true)
if echo "$OUTPUT" | grep -q "File incorrect.js is missing or has an incorrect header."; then
    echo "PASS: Test Case 3"
else
    echo "FAIL: Test Case 3 - Output: $OUTPUT"
    exit 1
fi

# --- Test Case 4: File with no header (fix-mode) ---
echo "--- Test Case 4: No header, with fix ---"
echo "function main() { /* ... */ }" > fix_me.go
EXPECTED_GO_HEADER=$(format_header_for_file go "$COMMON_HEADER_CONTENT")
OUTPUT=$(GITHUB_OUTPUT=/dev/null "$HARMONIZE_SCRIPT" "$COMMON_HEADER_CONTENT" "*.go" "true" 2>&1 || true)
if echo "$OUTPUT" | grep -q "Fixing header for fix_me.go..." && \
   echo "$OUTPUT" | grep -q "Header added to fix_me.go."; then
    if diff -q <(echo -e "$EXPECTED_GO_HEADER\nfunction main() { /* ... */ }") fix_me.go; then
        echo "PASS: Test Case 4"
    else
        echo "FAIL: Test Case 4 - File content mismatch"
        cat fix_me.go
        exit 1
    fi
else
    echo "FAIL: Test Case 4 - Output: $OUTPUT"
    exit 1
fi

# --- Test Case 5: Multiple file types, mixed compliance (fix-mode) ---
echo "--- Test Case 5: Multiple files, mixed compliance, with fix ---"
echo "<h1>HTML Content</h1>" > html_no_header.html
echo "/* CSS */" > css_incorrect_header.css # Incorrect, should be full header
echo -e "$(format_header_for_file py "$COMMON_HEADER_CONTENT")\nimport os" > py_correct.py

EXPECTED_HTML_HEADER=$(format_header_for_file html "$COMMON_HEADER_CONTENT")
EXPECTED_CSS_HEADER=$(format_header_for_file css "$COMMON_HEADER_CONTENT")

OUTPUT=$(GITHUB_OUTPUT=/dev/null "$HARMONIZE_SCRIPT" "$COMMON_HEADER_CONTENT" "*.html,*.css,*.py" "true" 2>&1 || true)

if echo "$OUTPUT" | grep -q "Fixing header for html_no_header.html..." && \
   echo "$OUTPUT" | grep -q "Fixing header for css_incorrect_header.css..." && \
   echo "$OUTPUT" | grep -q "File py_correct.py has the correct header."; then
    if diff -q <(echo -e "$EXPECTED_HTML_HEADER\n<h1>HTML Content</h1>") html_no_header.html && \
       diff -q <(echo -e "$EXPECTED_CSS_HEADER\n/* CSS */") css_incorrect_header.css; then
        echo "PASS: Test Case 5"
    else
        echo "FAIL: Test Case 5 - File content mismatch"
        cat html_no_header.html
        cat css_incorrect_header.css
        exit 1
    fi
else
    echo "FAIL: Test Case 5 - Output: $OUTPUT"
    exit 1
fi

# --- Test Case 6: No matching files ---
echo "--- Test Case 6: No matching files ---"
OUTPUT=$(GITHUB_OUTPUT=/dev/null "$HARMONIZE_SCRIPT" "$COMMON_HEADER_CONTENT" "*.xyz" "false" 2>&1 || true)
if echo "$OUTPUT" | grep -q "No files matched the provided patterns: \*.xyz"; then
    echo "PASS: Test Case 6"
else
    echo "FAIL: Test Case 6 - Output: $OUTPUT"
    exit 1
fi

# Clean up
cd - > /dev/null
rm -rf "$TEST_DIR"
echo "All tests passed!"
