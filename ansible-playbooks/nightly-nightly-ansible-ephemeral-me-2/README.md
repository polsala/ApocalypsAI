# Nightly Ansible Ephemeral Me

A whimsical-yet-useful Ansible playbook that broadcasts a temporary message to all managed hosts, then self-destructs after a configurable TTL. Perfect for announcements, reminders, or just to let your fleet know you're thinking of them.

## Features

- Broadcasts a message to all hosts in inventory
- Displays message with a configurable duration
- Automatically cleans up the message after TTL
- Includes a self-destruct mechanism for the playbook itself (optional)
- Generates a report of affected hosts

## Requirements

- Ansible 2.12+
- SSH access to managed hosts
- Python 3.8+ on control node

## Usage

1. Clone this playbook to your Ansible control node
2. Edit `inventory.ini` to include your hosts
3. Run the playbook:

```bash
ansible-playbook broadcast.yml -i inventory.ini
```

## Configuration

Edit the following variables in `broadcast.yml`:

- `ephemeral_message`: The message to broadcast
- `message_ttl`: Time in seconds before message disappears (default: 300)
- `self_destruct`: Set to `true` to delete the playbook after execution (default: false)

## Example Output

```
PLAY [Broadcast Ephemeral Message]

TASK [Gathering Facts]
ok: [host1.example.com]
ok: [host2.example.com]

TASK [Display ephemeral message]
changed: [host1.example.com]
changed: [host2.example.com]

TASK [Schedule cleanup]
changed: [host1.example.com]
changed: [host2.example.com]

PLAY RECAP
host1.example.com : ok=3    changed=2    unreachable=0    failed=0
host2.example.com : ok=3    changed=2    unreachable=0    failed=0
```

## License

MIT
