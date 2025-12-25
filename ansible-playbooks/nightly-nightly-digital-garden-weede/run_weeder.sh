#!/bin/bash
# Helper script to run the Digital Garden Weeder playbook

# Ensure Ansible is installed
if ! command -v ansible-playbook &> /dev/null
then
    echo "Ansible is not installed. Please install it first."
    echo "e.g., pip install ansible"
    exit 1
fi

INVENTORY="inventory.ini"
PLAYBOOK="prune_garden.yml"

echo "Running Digital Garden Weeder playbook..."
echo "To remove old config files, add --tags remove_old_configs"
echo ""

ansible-playbook -i "$INVENTORY" "$PLAYBOOK" "$@"

if [ $? -eq 0 ]; then
    echo ""
    echo "Digital Garden Weeding complete. Check 'weeding_report_*.txt' for details."
else
    echo ""
    echo "Digital Garden Weeding encountered issues."
fi
