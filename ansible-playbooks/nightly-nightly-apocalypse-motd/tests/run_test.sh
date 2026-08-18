#!/usr/bin/env bash
# Mock rationale: Simulate running the playbook and checking file creation without affecting system files.

set -e
PLAYBOOK_DIR=$(dirname "$0")/..
TMP_MOTD="./test_motd.txt"
# Run the playbook against localhost using a local connection.
ansible-playbook -i "$PLAYBOOK_DIR/src/inventory.ini" "$PLAYBOOK_DIR/src/playbook.yml" -e "motd_path=$TMP_MOTD" --connection=local --become=false
if [ -f "$TMP_MOTD" ]; then
  echo "MOTD file created successfully."
  # Clean up after test
  rm -f "$TMP_MOTD"
  exit 0
else
  echo "MOTD file was not created."
  exit 1
fi
