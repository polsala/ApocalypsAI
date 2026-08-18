#!/usr/bin/env bash
set -euo pipefail

# Create a temporary known_hosts file
tmpfile=$(mktemp)
cat > "$tmpfile" <<'EOF'
# Sample known_hosts
example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1
example.com,192.168.1.1 ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2
example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1
another.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB3
# End of file
EOF

# Expected output after deduplication (first occurrence kept)
read -r -d '' expected <<'EOT'
# Sample known_hosts
example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1
example.com,192.168.1.1 ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2
another.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB3
# End of file
EOT

# Run script without -i, capture stdout
output=$(../src/deduper.sh "$tmpfile")
if [[ "$output" != "$expected" ]]; then
  echo "Test failed: stdout output does not match expected"
  echo "Got:"
  echo "$output"
  echo "Expected:"
  echo "$expected"
  exit 1
fi

# Run script with -i (in‑place)
../src/deduper.sh -i "$tmpfile"
inplace_output=$(cat "$tmpfile")
if [[ "$inplace_output" != "$expected" ]]; then
  echo "Test failed: in‑place file content does not match expected"
  exit 1
fi

echo "All tests passed."
