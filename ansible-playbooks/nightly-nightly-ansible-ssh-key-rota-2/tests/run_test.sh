#!/usr/bin/env bash
set -e

# Mock rationale: Use a temporary directory to avoid polluting repo
TMPDIR=$(mktemp -d)
export ANSIBLE_HOST_KEY_CHECKING=False

# Run playbook in check mode
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml --check -e "key_dir=$TMPDIR"

# Run playbook for real
ansible-playbook -i src/inventory.ini src/rotate_ssh_keys.yml -e "key_dir=$TMPDIR"

# Verify key files exist
if [[ -f "$TMPDIR/id_rsa" && -f "$TMPDIR/id_rsa.pub" ]]; then
  echo "Test passed: keys generated"
  exit 0
else
  echo "Test failed: keys not found"
  exit 1
fi

