#!/bin/bash
set -euo pipefail

echo "--- Running Digital Garden Gnome Keeper Tests ---"

# Define inventory for tests
TEST_INVENTORY="tests/inventory_test.ini"
MAIN_PLAYBOOK="src/gnome_keeper.yml"
CLEANUP_PLAYBOOK="tests/cleanup.yml"
VERIFY_PLAYBOOK="tests/verify.yml"

# Check if ansible-playbook is available
if ! command -v ansible-playbook &> /dev/null
then
    echo "Error: ansible-playbook command not found. Please install Ansible."
    exit 1
fi

echo "1. Cleaning up previous test artifacts..."
ansible-playbook -i "${TEST_INVENTORY}" "${CLEANUP_PLAYBOOK}"

echo "2. Running the main Digital Garden Gnome Keeper playbook..."
ansible-playbook -i "${TEST_INVENTORY}" "${MAIN_PLAYBOOK}"

echo "3. Verifying the deployed state..."
ansible-playbook -i "${TEST_INVENTORY}" "${VERIFY_PLAYBOOK}"

echo "4. Cleaning up test artifacts after verification..."
ansible-playbook -i "${TEST_INVENTORY}" "${CLEANUP_PLAYBOOK}"

echo "--- All tests passed! ---"
