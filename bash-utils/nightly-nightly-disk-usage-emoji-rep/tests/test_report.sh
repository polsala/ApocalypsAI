#!/usr/bin/env bash
set -euo pipefail

# Helper to run the script with mocked df/du outputs
run_report() {
  local mock_df_line="$1"
  local mock_du_line="$2"
  local path_arg="${3:-.}"

  # Create temporary directory for mock binaries
  TMPDIR=$(mktemp -d)

  # Mock df
  cat >"$TMPDIR/df" <<'EOF'
#!/usr/bin/env bash
# Mock df: prints header then the line supplied via env var
echo "Filesystem 1024-blocks Used Available Use% Mounted on"
echo "$MOCK_DF_LINE"
EOF
  chmod +x "$TMPDIR/df"

  # Mock du
  cat >"$TMPDIR/du" <<'EOF'
#!/usr/bin/env bash
# Mock du: prints the line supplied via env var
echo "$MOCK_DU_LINE"
EOF
  chmod +x "$TMPDIR/du"

  # Export variables consumed by the mock scripts
  export MOCK_DF_LINE="$mock_df_line"
  export MOCK_DU_LINE="$mock_du_line"

  # Prepend mock directory to PATH and invoke the utility
  PATH="$TMPDIR:$PATH" "$PWD/../src/report.sh" "$path_arg"

  # Clean up
  rm -rf "$TMPDIR"
}

# Test low usage (<10%)
output=$(run_report "10240 500 9750 5% /" "5K\t./low" ".")
if [[ "$output" != "🟢 5K ."* ]]; then
  echo "Low usage test failed: $output"
  exit 1
fi

# Test moderate usage (10‑50%)
output=$(run_report "10240 3000 7240 30% /" "3M\t./mid" ".")
if [[ "$output" != "🟡 3M ."* ]]; then
  echo "Moderate usage test failed: $output"
  exit 1
fi

# Test high usage (>50%)
output=$(run_report "10240 8000 2240 78% /" "8M\t./high" ".")
if [[ "$output" != "🔴 8M ."* ]]; then
  echo "High usage test failed: $output"
  exit 1
fi

echo "All tests passed."
