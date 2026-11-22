# nightly-server-motd-blesser

## Whimsical Server MOTD Blesser

This Ansible playbook is designed to bring a touch of whimsy and positivity to your servers by updating their Message Of The Day (MOTD) with a randomly selected, uplifting message. It's a small gesture to brighten the day of anyone logging in, reminding them that even in the digital realm, there's room for a little magic.

### Features

*   **Randomized Messages**: Selects a new message from a predefined list on each run.
*   **OS-Aware Deployment**: Automatically adapts to Debian-based systems (using `/etc/update-motd.d/`) and other Linux distributions (using `/etc/motd`).
*   **Customizable**: Easily add or modify the list of whimsical messages.

### Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target servers with `sudo` privileges.

2.  **Inventory**: Create an `inventory.ini` file (or use an existing one) listing your target servers. An example `src/inventory.ini` is provided.

    ```ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

3.  **Customize Messages (Optional)**: Edit `src/vars/messages.yml` to add your own whimsical messages.

    ```yaml
    ---
messages:
  - "May your uptime be long and your logs be clear!"
  - "This server is powered by stardust and good intentions."
  # ... more messages
    ```

4.  **Run the Playbook**: Execute the playbook using `ansible-playbook`:

    ```bash
    ansible-playbook -i src/inventory.ini src/motd_blesser.yml
    ```

    This will connect to all hosts defined in your inventory under the `[servers]` group, select a random message, and update their MOTD.

### Testing

To ensure the playbook works as expected, a test playbook `tests/test_motd_blesser.yml` is provided. This test runs against `localhost` and verifies that the MOTD file is created with a specific, deterministic message.

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_motd_blesser.yml
```

The test playbook will:
1.  Run the main `motd_blesser.yml` playbook, overriding the random message selection with a fixed test message.
2.  Assert that the correct MOTD file (`/etc/motd` or `/etc/update-motd.d/99-whimsical-motd`) contains the expected test message.
3.  Clean up the created MOTD files.
