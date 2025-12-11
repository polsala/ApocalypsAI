# Ephemeral Message Broadcast

This utility provides an Ansible playbook that broadcasts a temporary message to a set of hosts. The message is written to a file under `/tmp/ephemeral_messages/<host>/message.txt` and automatically removed after a configurable time‑to‑live (TTL).

## How it works

1. **broadcast.yml** creates the target directory and writes the message.
2. **cleanup.yml** finds and deletes messages older than the specified TTL.

## Usage

```bash
# Edit inventory.ini to list your hosts (default uses localhost aliases)
ansible-playbook -i inventory.ini broadcast.yml -e "message='Hello world' ttl_seconds=3600"
# When the TTL expires, run the cleanup playbook (or schedule it via cron)
ansible-playbook -i inventory.ini cleanup.yml -e "ttl_seconds=3600"
```

## Testing

Run the provided test script:

```bash
bash tests/test_broadcast.sh
```

It will verify that the message file is created and subsequently removed.
