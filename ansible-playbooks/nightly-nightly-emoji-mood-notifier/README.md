# Emoji Mood Notifier

A whimsical Ansible playbook that installs a tiny script which prints a random emoji mood to the console each morning via a cron job. Useful for adding a splash of joy to your server's daily routine.

## Requirements

- Ansible 2.9+
- Target host with cron support

## Usage

```bash
ansible-playbook -i inventory.ini src/main.yml
```

The playbook will:

1. Copy `notify.sh` to `/usr/local/bin/emoji_mood_notifier.sh`.
2. Make it executable.
3. Create a daily cron job at 09:00 that runs the script.

## Customization

Edit `src/notify.sh` to change the list of emojis or the output format.
