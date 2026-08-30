#!/bin/bash
set -euo pipefail

echo "Running Ansible syntax check..."
ansible-playbook ../src/fortify_bunker.yml --syntax-check

echo "Running Ansible check mode with mocked inventory and variables..."

# Create a temporary inventory file for testing
# Mock rationale: Provides a minimal, local inventory for testing without real hosts.
cat <<EOF > /tmp/test_inventory.ini
[bunkers]
localhost ansible_connection=local
EOF

# Create temporary mock files for MOTD and unattended-upgrades config
# Mock rationale: Prevents actual system file modifications during check mode.
touch /tmp/test_motd
touch /tmp/test_20auto-upgrades

# Run the playbook in check mode with mocked facts and paths
# Mock rationale:
# - ansible_connection=local: Ensures playbook runs against localhost without SSH.
# - gather_facts=no: Prevents actual fact gathering for deterministic testing.
# - ansible_os_family=Debian: Simulates a Debian-like system for apt tasks.
# - motd_dest_path, auto_upgrades_config_path: Use temporary paths to avoid actual system modification.
# - check_mode: Runs without making actual changes, reporting what *would* happen.
# - --diff: Shows potential changes, useful for debugging check mode.
ansible-playbook ../src/fortify_bunker.yml \
  -i /tmp/test_inventory.ini \
  --extra-vars "ansible_connection=local gather_facts=no ansible_os_family=Debian motd_dest_path=/tmp/test_motd auto_upgrades_config_path=/tmp/test_20auto-upgrades" \
  --check \
  --diff \
  | tee /tmp/ansible_check_output.log

# Assertions based on check mode output
# Mock rationale: Check if the playbook *would* report changes for key tasks.
# This is a basic check to ensure the playbook logic is triggered and tasks are correctly defined.
if grep -q "changed=1.*name='Ensure apt cache is updated'" /tmp/ansible_check_output.log && \
   grep -q "changed=1.*name='Install essential security tools (fail2ban, ufw)'" /tmp/ansible_check_output.log && \
   grep -q "changed=1.*name='Enable UFW and set default rules'" /tmp/ansible_check_output.log && \
   grep -q "changed=1.*name='Set the Digital Bunker MOTD'" /tmp/ansible_check_output.log; then
  echo "Check mode test PASSED: Expected changes were reported."
else
  echo "Check mode test FAILED: Expected changes were NOT reported."
  exit 1
fi

# Clean up temporary files
rm /tmp/test_inventory.ini /tmp/test_motd /tmp/test_20auto-upgrades /tmp/ansible_check_output.log

echo "All tests PASSED."
