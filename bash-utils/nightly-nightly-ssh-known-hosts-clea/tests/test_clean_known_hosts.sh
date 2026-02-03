#!/usr/bin/env bash
set -euo pipefail

# Create a temporary known_hosts file with intentional duplicates
tmpfile=$(mktemp)
cat > "$tmpfile" <<'EOF'
example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1
example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1
github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE
github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE
gitlab.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD2
EOF

# --- Dry‑run test ---
output=$(../src/clean_known_hosts.sh --dry-run "$tmpfile")
expected="Dry run: 2 duplicate entries would be removed from $tmpfile."
if [[ "$output" != "$expected" ]]; then
  echo "Dry‑run test failed"
  echo "Got: $output"
  echo "Expected: $expected"
  exit 1
fi

# --- Actual cleaning test ---
../src/clean_known_hosts.sh "$tmpfile"
# After cleaning, the file should contain exactly 3 unique lines
lines=$(wc -l < "$tmpfile")
if [[ "$lines" -ne 3 ]]; then
  echo "Cleaning test failed: expected 3 lines, got $lines"
  exit 1
fi

echo "All tests passed."
