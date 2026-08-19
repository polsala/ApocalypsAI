#!/usr/bin/env bash
set -e

# Helper to run the utility with a mocked df output
run_test() {
  local mock_data="$1"
  local expected_exit="$2"
  local expected_output="$3"

  tmpdir=$(mktemp -d)
  # Create a mock df that prints the supplied data regardless of arguments
  cat > "$tmpdir/df" <<'EOF'
#!/usr/bin/env bash
cat "$DF_MOCK_DATA"
EOF
  chmod +x "$tmpdir/df"

  export DF_MOCK_DATA="$tmpdir/mock_data.txt"
  echo "$mock_data" > "$DF_MOCK_DATA"

  # Prepend mock directory to PATH so our df is used
  PATH="$tmpdir:$PATH" "$PWD/../src/disk-usage-alert.sh" 80 > out.txt 2>&1
  exit_code=$?

  if [ "$exit_code" -ne "$expected_exit" ]; then
    echo "FAIL: expected exit $expected_exit, got $exit_code"
    cat out.txt
    exit 1
  fi

  if [ -n "$expected_output" ]; then
    if ! grep -q "$expected_output" out.txt; then
      echo "FAIL: expected output not found"
      cat out.txt
      exit 1
    fi
  fi

  rm -rf "$tmpdir" out.txt
}

# Test 1: No filesystem exceeds the default 80% threshold
run_test "$(cat <<'DATA'
Filesystem Size Used Avail Use% Mounted on
/dev/sda1 100G 40G 60G 40% /
DATA
)" 0 ""

# Test 2: One filesystem exceeds the threshold
run_test "$(cat <<'DATA'
Filesystem Size Used Avail Use% Mounted on
/dev/sda1 100G 90G 10G 90% /
DATA
)" 1 "Warning: / is 90% full (threshold 80%)"

echo "All tests passed"
