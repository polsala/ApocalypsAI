#!/usr/bin/env bash
set -e
# Run the playbook in check mode to verify syntax and logic without making changes
ansible-playbook -i inventory.ini rotate_ssh_keys.yml --check -e "target_hosts=localhost cleanup_private_key=false"
echo "Test passed"
