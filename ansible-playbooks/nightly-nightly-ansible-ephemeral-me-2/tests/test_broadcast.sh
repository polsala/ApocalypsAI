#!/bin/bash
# Test script for Nightly Ansible Ephemeral Me

set -e

TEST_DIR="/tmp/apocalypsai_test"
MESSAGE_FILE="$TEST_DIR/apocalypsai_ephemeral_message"
CLEANUP_SCRIPT="$TEST_DIR/apocalypsai_cleanup.sh"
REPORT_FILE="$TEST_DIR/apocalypsai_report_test.txt"

# Mock rationale: Create test directory structure
mkdir -p "$TEST_DIR"

# Mock rationale: Create mock inventory
cat > inventory_test.ini << EOF
[all_hosts]
testhost ansible_connection=local ansible_python_interpreter=$(which python3)
EOF

# Mock rationale: Create mock ansible.cfg for testing
cat > ansible.cfg << EOF
[defaults]
host_key_checking = False
inventory = inventory_test.ini
remote_user = root
EOF

# Mock rationale: Create test playbook with modified paths
sed 's|/tmp/apocalypsai_|$TEST_DIR/apocalypsai_|g' broadcast.yml > test_broadcast.yml

# Mock rationale: Replace variables with test values
sed -i 's|message_ttl: 300|message_ttl: 5|g' test_broadcast.yml
sed -i 's|self_destruct: false|self_destruct: false|g' test_broadcast.yml

# Mock rationale: Run the playbook in test mode
echo "=== Running Ansible Ephemeral Me Test ==="
ansible-playbook -i inventory_test.ini test_broadcast.yml --check --diff

# Mock rationale: Verify files were created
if [ -f "$MESSAGE_FILE" ]; then
    echo "✓ Message file created successfully"
else
    echo "✗ Message file not found"
    exit 1
fi

if [ -f "$CLEANUP_SCRIPT" ]; then
    echo "✓ Cleanup script created successfully"
else
    echo "✗ Cleanup script not found"
    exit 1
fi

if [ -f "$REPORT_FILE" ]; then
    echo "✓ Report file created successfully"
else
    echo "✗ Report file not found"
    exit 1
fi

# Mock rationale: Verify message content
EXPECTED_LINES=5
ACTUAL_LINES=$(wc -l < "$MESSAGE_FILE")
if [ "$ACTUAL_LINES" -ge "$EXPECTED_LINES" ]; then
    echo "✓ Message content verified"
else
    echo "✗ Message content incomplete"
    exit 1
fi

# Mock rationale: Test cleanup after TTL
echo "=== Testing cleanup mechanism ==="
# Run cleanup script
bash "$CLEANUP_SCRIPT"

# Verify cleanup
if [ ! -f "$MESSAGE_FILE" ]; then
    echo "✓ Message file cleaned up successfully"
else
    echo "✗ Message file still exists"
    exit 1
fi

# Mock rationale: Cleanup test environment
rm -rf "$TEST_DIR"
rm -f inventory_test.ini ansible.cfg test_broadcast.yml

# Mock rationale: Run syntax check on original playbook
echo "=== Syntax validation ==="
ansible-playbook --syntax-check broadcast.yml

if [ $? -eq 0 ]; then
    echo "✓ Playbook syntax is valid"
else
    echo "✗ Playbook syntax errors found"
    exit 1
fi

# Mock rationale: Validate inventory format
echo "=== Inventory validation ==="
ansible-inventory -i inventory.ini --list > /dev/null

if [ $? -eq 0 ]; then
    echo "✓ Inventory format is valid"
else
    echo "✗ Inventory format errors found"
    exit 1
fi

# Mock rationale: Test cleanup script syntax
echo "=== Cleanup script validation ==="
bash -n cleanup.sh

if [ $? -eq 0 ]; then
    echo "✓ Cleanup script syntax is valid"
else
    echo "✗ Cleanup script syntax errors found"
    exit 1
fi

# Mock rationale: Verify all test assertions passed
echo "\n=== All tests passed! ==="
echo "✓ Playbook syntax validation"
echo "✓ Inventory format validation"
echo "✓ Cleanup script syntax validation"
echo "✓ Message file creation"
echo "✓ Cleanup script creation"
echo "✓ Report file creation"
echo "✓ Message content verification"
echo "✓ Automatic cleanup mechanism"
echo "\nNightly Ansible Ephemeral Me is ready for production use!"

exit 0
