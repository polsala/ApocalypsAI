#!/usr/bin/env bash
set -euo pipefail

# Determine the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the playbook in check mode to ensure syntax and dry‑run success
ansible-playbook -i "${SCRIPT_DIR}/../inventory.ini" "${SCRIPT_DIR}/../apt_cleanup.yml" --check

echo "Test passed: apt_cleanup.yml runs successfully in check mode."
