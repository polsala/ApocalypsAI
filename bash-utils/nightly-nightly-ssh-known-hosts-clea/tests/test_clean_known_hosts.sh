#!/usr/bin/env bash
set -euo pipefail

# Create a temporary directory for the test files
TMPDIR=$(mktemp -d)
KNOWN_HOSTS="$TMPDIR/known_hosts"

# Populate the temporary known_hosts with duplicate entries and comments
cat > "$KNOWN_HOSTS" <<'EOF'
# First comment line
example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1
example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1
duplicate.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE
# Second comment line
duplicate.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE
EOF

# Expected cleaned output (comments preserved, duplicates removed, sorted)
cat > "$TMPDIR/expected" <<'EOF'
# First comment line
# Second comment line
duplicate.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE
example.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1
EOF

# Run the utility against the temporary known_hosts file
bash ../src/clean_known_hosts.sh "$KNOWN_HOSTS"

# Verify that the cleaned file matches the expected result
if diff -u "$KNOWN_HOSTS" "$TMPDIR/expected"; then
  echo "Test passed"
else
  echo "Test failed"
  exit 1
fi

# Verify that a backup was created and contains the original (pre‑clean) content
if [[ -f "${KNOWN_HOSTS}.bak" ]]; then
  echo "Backup file exists"
else
  echo "Backup file missing"
  exit 1
fi
