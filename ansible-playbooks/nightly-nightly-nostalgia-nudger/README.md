# Nightly Nostalgia Nudger

## Overview

The `Nightly Nostalgia Nudger` is an Ansible playbook designed to deploy and maintain a 'comfort file' on target systems. This file contains whimsical, inspirational, or simply comforting messages, ensuring a consistent and personalized touch across your development environments, servers, or personal workstations. It's a gentle reminder from the ApocalypsAI community that even amidst chaos, a little bit of whimsy can go a long way.

## Features

- **Idempotent Deployment**: Ensures the comfort file exists and its content matches the defined template, only making changes when necessary.
- **Customizable Content**: Easily modify the message title, content, and author via `vars/main.yml` and `templates/comfort_message.j2`.
- **Directory Management**: Automatically creates the target directory if it doesn't exist.
- **User-Specific Paths**: Defaults to placing the file in the user's home directory (`~/.comfort_message.txt`).
- **Optional Timestamp**: Includes a generation timestamp in the file, which can be toggled off for strict idempotency.

## Prerequisites

- **Ansible**: Installed on the control machine.
- **Target Systems**: Any Linux-based system reachable by Ansible.

## Usage

1.  **Define your inventory**: Create or update an `inventory.ini` file with your target hosts.
    ```ini
    [my_servers]
    server1.example.com
    server2.example.com

    [local]
    localhost ansible_connection=local
    ```

2.  **Customize the message (Optional)**: Edit `vars/main.yml` and `templates/comfort_message.j2` to personalize your comfort message.

3.  **Run the playbook**:
    ```bash
    ansible-playbook -i inventory.ini nostalgia_nudger.yml
    ```

    To run it against a specific group (e.g., `local`):
    ```bash
    ansible-playbook -i inventory.ini nostalgia_nudger.yml --limit local
    ```

## Configuration

Edit `vars/main.yml` to change the default settings:

```yaml
comfort_file_path: "{{ ansible_user_dir | default('/tmp') }}/.comfort_message.txt"
comfort_message_title: "A Whisper from the Void"
comfort_message_content: |
  "Even in the darkest timelines, a spark of whimsy can ignite hope.
  Remember to hydrate, recalibrate, and embrace the glorious chaos."
comfort_message_author: "ApocalypsAI Integrator"
include_timestamp: true # Set to false for strict idempotency (no timestamp)
```

## Testing

To run the included tests, ensure Ansible is installed and execute:

```bash
ansible-playbook -i inventory.ini tests/test_nostalgia_nudger.yml
```

This will run a local test that creates, verifies, and cleans up a temporary comfort file, ensuring the playbook is idempotent and functions as expected.
