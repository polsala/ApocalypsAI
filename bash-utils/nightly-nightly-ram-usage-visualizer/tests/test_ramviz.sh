#!/usr/bin/env bash
# Tests for nightly-ram-usage-visualizer

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/ramviz.sh"

# Helper to run the script with a temporary meminfo file and verify output via a regex
run_test() {
  local meminfo_content="$1"
  local expected_regex="$2"
  local tmpfile
  tmpfile=$(mktemp)
  echo "$meminfo_content" > "$tmpfile"
  output=$("$SCRIPT" "$tmpfile")
  rm "$tmpfile"
  if [[ ! "$output" =~ $expected_regex ]]; then
    echo "Test failed. Output:" >&2
    echo "$output" >&2
    echo "Expected regex: $expected_regex" >&2
    exit 1
  fi
}

# Test low usage (10%) – expect a mostly empty bar
run_test "MemTotal:       8000000 kB
MemAvailable:   7200000 kB" "^RAM Usage: 10% \[███─{17}\]$"

# Test high usage (90%) – should include a motivational quote line
tmp_high=$(mktemp)
echo "MemTotal: 8000000 kB
MemAvailable: 800000 kB" > "$tmp_high"
output_high=$("$SCRIPT" "$tmp_high")
rm "$tmp_high"
first_line=$(echo "$output_high" | head -n1)
second_line=$(echo "$output_high" | tail -n+2 | head -n1)
if [[ ! "$first_line" =~ ^RAM\ Usage:\ 90%\ \[██████████───────\]$ ]]; then
  echo "High‑usage bar test failed" >&2
  exit 1
fi
if [[ -z "$second_line" ]]; then
  echo "Expected motivational quote but got none" >&2
  exit 1
fi

# Test handling of a non‑readable file
if "$SCRIPT" "/nonexistent/path" 2>/dev/null; then
  echo "Expected failure on unreadable file but script succeeded" >&2
  exit 1
fi

# Test handling of malformed meminfo
tmp_bad=$(mktemp)
echo "Invalid content" > "$tmp_bad"
if "$SCRIPT" "$tmp_bad" 2>/dev/null; then
  echo "Expected failure on malformed meminfo but script succeeded" >&2
  rm "$tmp_bad"
  exit 1
fi
rm "$tmp_bad"

echo "All tests passed."
