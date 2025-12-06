# Nightly Morale Dispatcher

## Overview

The `nightly-morale-dispatcher` is an Ansible playbook designed to inject a dose of whimsy and encouragement into your post-apocalyptic infrastructure. It randomly selects a morale-boosting message or survival tip from a predefined list and deploys it to specified target files on your remote 'outposts' (servers).

This utility is perfect for keeping spirits high, reminding your automated systems of their purpose, or simply adding a touch of personality to your server MOTDs or custom status files.

## Features

*   **Randomized Messages**: Selects a new message from a curated list for each deployment.
*   **Configurable Target**: Easily specify the directory and file where messages should be deployed.
*   **Idempotent**: Ensures the target file is updated only when the message changes, or if forced.
*   **Simple Deployment**: Uses standard Ansible modules for easy integration into existing workflows.

## Usage

### Prerequisites

*   Ansible installed (version 2.9+ recommended).
*   SSH access to your target hosts (if not running locally).

### Files

*   `morale_dispatcher.yml`: The main Ansible playbook.
*   `inventory.ini`: An example inventory file listing your target 'outposts'.
*   `vars/messages.yml`: Contains the list of morale messages.

### Configuration

1.  **`inventory.ini`**: Update this file with the IP addresses or hostnames of your target servers. For local testing, `localhost` is included.
    ```ini
    [outposts]
    localhost ansible_connection=local
    # outpost1.example.com
    # outpost2.example.com
    ```

2.  **`vars/messages.yml`**: Customize the `morale_messages` list with your own whimsical or practical tips.
    ```yaml
    morale_messages:
      - "Stay vigilant, wanderer! The dawn always follows the darkest night."
      - "Remember to hydrate! Even the dust has a thirst."
      # ... more messages
    ```

3.  **Target File**: By default, messages are deployed to `/etc/motd.d/apocalypsai_motd`. You can override this using extra variables:
    *   `target_motd_dir`: The directory where the message file will reside (e.g., `/tmp`).
    *   `target_motd_file`: The full path to the message file (e.g., `/tmp/my_custom_message`).

### Running the Playbook

To dispatch a morale message to all hosts in your inventory:

```bash
ansible-playbook -i inventory.ini morale_dispatcher.yml
```

To dispatch to a specific host (e.g., `localhost`):

```bash
ansible-playbook -i inventory.ini morale_dispatcher.yml --limit localhost
```

To deploy to a custom location (e.g., `/home/user/motd.txt`):

```bash
ansible-playbook -i inventory.ini morale_dispatcher.yml \
  -e "target_motd_dir=/home/user" \
  -e "target_motd_file=/home/user/motd.txt"
```

## Testing

To run the automated tests for this playbook, execute the `test_morale_dispatcher.yml` playbook:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_morale_dispatcher.yml
```

This will run the main playbook against `localhost` in a controlled environment and assert that a message was successfully deployed to a temporary file and its content is valid.
