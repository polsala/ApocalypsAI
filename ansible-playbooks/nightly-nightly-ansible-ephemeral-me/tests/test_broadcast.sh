#!/usr/bin/env bash
set -e

# Mock rationale: Ensure a clean environment before test
rm -rf /tmp/ephemeral_messages

# Run the broadcast playbook with a short TTL
ansible-playbook -i inventory.ini broadcast.yml -e "message='Test Message' ttl_seconds=0"

# Verify the message file was created
if [ ! -f /tmp/ephemeral_messages/host1/message.txt ]; then
  echo "FAIL: Message file not created on host1"
  exit 1
fi

# Run the cleanup playbook which should delete the file immediately (TTL=0)
ansible-playbook -i inventory.ini cleanup.yml -e "ttl_seconds=0"

# Verify the message file was removed
if [ -f /tmp/ephemeral_messages/host1/message.txt ]; then
  echo "FAIL: Cleanup did not remove the message file"
  exit 1
fi

echo "PASS: Ephemeral message broadcast and cleanup work as expected"
