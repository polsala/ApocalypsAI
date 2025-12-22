#!/bin/bash
set -euo pipefail

echo "Running Nightly Beacon Network Synchronizer tests..."

# Ensure Ansible is installed
if ! command -v ansible-playbook &> /dev/null
then
    echo "Ansible is not installed. Please install it to run tests."
    exit 1
fi

# Run the test playbook
# The test playbook itself handles setup, execution of the main playbook, and cleanup.
# We just need to ensure it runs without errors.
ansible-playbook -i tests/inventory_test.ini tests/test_beacon_sync.yml

if [ $? -eq 0 ]; then
    echo "Nightly Beacon Network Synchronizer tests PASSED!"
else
    echo "Nightly Beacon Network Synchronizer tests FAILED!"
    exit 1
fi
