# Nightly MOTD Morale Booster

This Ansible playbook deploys a whimsical, morale-boosting message or a practical survival tip to the Message of the Day (MOTD) on your target servers. In these trying times, a little digital cheer or a timely reminder can go a long way!

## Features

*   **Whimsical Messages**: Delivers a random, pre-defined message to `/etc/motd`.
*   **Customizable**: Easily add or modify the list of messages.
*   **Idempotent**: Ensures the MOTD is updated only when the message changes.
*   **Permissions Controlled**: Sets appropriate permissions for the MOTD file.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate privileges (e.g., `sudo`).

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use an existing one) listing your target servers.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```

2.  **Customize messages (Optional)**:
    Edit `src/vars/motd_messages.yml` to add, remove, or modify the list of messages.

    ```yaml
    # src/vars/motd_messages.yml
    motd_messages:
      - "Remember, even in the darkest void, a byte of hope shines bright!"
      - "Your code is compiling, and so is your destiny. Stay strong!"
      - "Did you remember to hydrate? Your brain (and server) will thank you."
      - "The only thing constant is change... and hopefully, your backups."
      - "May your logs be clear and your coffee strong."
    ```

3.  **Run the playbook**:

    ```bash
    ansible-playbook -i inventory.ini src/deploy_motd.yml
    ```

    This will connect to your servers, pick a random message, and update their `/etc/motd` file.

## Example Output on Server Login

```
Welcome to web1.example.com!
Remember, even in the darkest void, a byte of hope shines bright!
```

## Testing

To run the included tests, you'll need `ansible-lint` (optional, for best practices) and `ansible-playbook`. The test playbook `tests/test_deploy_motd.yml` will run the main playbook with a *specific* message for deterministic verification.

```bash
# Ensure ansible-lint is installed: pip install ansible-lint
ansible-playbook -i tests/inventory_test.ini tests/test_deploy_motd.yml
```

The test playbook will assert that the `/etc/motd` file contains the expected test message.
