# Nightly Morale Broadcast

**Purpose**: In a world of temporal rifts and wandering wastelands, morale is a scarce resource. This Ansible playbook selects a random inspirational quote and posts it to a Slack channel (or any webhook‑compatible endpoint) so your crew can stay hopeful.

## Features

- Randomly picks a quote from a curated list.
- Renders a nicely formatted message using a Jinja2 template.
- Sends the message via the `uri` module to a configurable webhook URL.
- Fully idempotent – running the playbook multiple times will post a new quote each run.

## Requirements

- Ansible 2.12+ installed on the control node.
- Access to the target host (can be `localhost`).
- A Slack Incoming Webhook URL (or any HTTP endpoint that accepts a JSON payload with a `text` field).

## Quick Start

```bash
# Clone the repository (or copy the utility folder) and cd into it
cd ansible-playbooks/nightly-morale-broadcast

# Install any required collections (none needed beyond core)

# Run the playbook (replace the webhook URL with your own)
ansible-playbook -i inventory src/broadcast.yml \
  -e "slack_webhook_url=https://hooks.slack.com/services/XXXXX/XXXXX/XXXXX"
```

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `slack_webhook_url` | The full URL of the Slack Incoming Webhook (or compatible endpoint). | *required* |
| `quote_list` | List of quotes to choose from. | See `src/vars/main.yml` |

## Customisation

Edit `src/vars/main.yml` to add, remove, or modify the quotes. The template `src/templates/message.j2` can be tweaked to change the message layout.

## Testing

Run the deterministic test suite with:

```bash
ansible-playbook -i inventory tests/test_broadcast.yml
```

The test ensures that a message file is generated and contains one of the expected quotes.
