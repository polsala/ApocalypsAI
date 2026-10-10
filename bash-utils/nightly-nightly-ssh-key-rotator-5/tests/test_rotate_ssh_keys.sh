#!/usr/bin/env bash
set -euo pipefail

# Helper for assertions
assert_eq() {
  local expected="$1"
  local actual="$2"
  local msg="$3"
  if [[ "$expected" != "$actual" ]]; then
    echo "FAIL: $msg (expected='$expected', actual='$actual')"
    exit 1
  fi
}

# Create a temporary HOME directory
TMP_HOME=$(mktemp -d)
export HOME="$TMP_HOME"
mkdir -p "$HOME/.ssh"

# Mock existing SSH keys (dummy content)
echo "old private key" > "$HOME/.ssh/id_rsa"
echo "old public key" > "$HOME/.ssh/id_rsa.pub"

# Freeze the timestamp for reproducibility
export DATE_OVERRIDE="20230101010101"

# Run the utility
output=$(bash "../src/rotate_ssh_keys.sh" 2>&1)

# Verify backup directory exists
backup_dir="$HOME/.ssh/backup_20230101010101"
if [[ ! -d "$backup_dir" ]]; then
  echo "FAIL: Backup directory not created"
  exit 1
fi

# Verify old keys were copied
assert_eq "old private key" "$(cat "$backup_dir/id_rsa")" "Backup of private key"
assert_eq "old public key" "$(cat "$backup_dir/id_rsa.pub")" "Backup of public key"

# Verify new keys exist and are not the old content
new_private=$(cat "$HOME/.ssh/id_rsa")
new_public=$(cat "$HOME/.ssh/id_rsa.pub")
if [[ "$new_private" == "old private key" ]] || [[ -z "$new_private" ]]; then
  echo "FAIL: New private key not generated correctly"
  exit 1
fi
if [[ "$new_public" == "old public key" ]] || [[ -z "$new_public" ]]; then
  echo "FAIL: New public key not generated correctly"
  exit 1
fi

# Verify output contains one of the expected quotes
expected_quotes=(
  "The night is dark, but your keys are bright."
  "Rotating keys, like rotating the earth—endless."
  "Even the wasteland respects a fresh key pair."
  "Secure today, survive tomorrow."
)
match=0
for q in "${expected_quotes[@]}"; do
  if [[ "$output" == *"$q"* ]]; then
    match=1
    break
  fi
done
if [[ $match -ne 1 ]]; then
  echo "FAIL: Output does not contain a known quote"
  echo "Output was: $output"
  exit 1
fi

echo "PASS: All checks succeeded"
