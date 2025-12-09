#!/usr/bin/env bash
# Mock rationale: deterministic end‑to‑end test using only local resources
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Step 1: prepare test files
"${SCRIPT_DIR}/setup.sh"

# Step 2: run the playbook against the local inventory
ansible-playbook -i "${SCRIPT_DIR}/../inventory.ini" "${SCRIPT_DIR}/../playbook.yml"

# Step 3: verify that the archive was created and contains the expected files
if [[ -f "/tmp/ghosts.tar.gz" ]]; then
  # List contents of the tarball (quietly) and ensure both ghost files are present
  if tar -tzf "/tmp/ghosts.tar.gz" | grep -q "spooky1.ghost" && tar -tzf "/tmp/ghosts.tar.gz" | grep -q "spooky2.ghost"; then
    echo "TEST SUCCESS: Ghost archive created at /tmp/ghosts.tar.gz"
  else
    echo "TEST FAILURE: Archive missing expected ghost files" >&2
    exit 1
  fi
else
  echo "TEST FAILURE: Archive /tmp/ghosts.tar.gz was not created" >&2
  exit 1
fi

# Step 4: clean up
"${SCRIPT_DIR}/cleanup.sh"
