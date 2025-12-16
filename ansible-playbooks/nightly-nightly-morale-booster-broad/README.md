# Nightly Morale Booster Broadcast

An Ansible playbook to uplift the spirits of your community terminals (servers) by broadcasting whimsical, morale-boosting messages daily. Because even in the post-apocalyptic wasteland, a little cheer goes a long way!

## Features

*   **Whimsical Messages**: Distributes a random, pre-defined morale-boosting message.
*   **MOTD Integration**: Updates the `/etc/motd` (Message Of The Day) or a custom file on target hosts.
*   **Idempotent**: Ensures the message block is managed without duplication.
*   **Customizable**: Easily add or modify morale messages in `vars/morale_messages.yml`.

## Prerequisites

*   **Ansible**: Installed on your control machine.
*   **Target Hosts**: Accessible via SSH from your control machine.
*   **Sudo/Become**: The Ansible user on target hosts must have `sudo` privileges to modify `/etc/motd` or other system files.

## Usage

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-morale-booster-broadcast
    ```

2.  **Configure your inventory**:
    Edit `inventory.ini` to list your target "community terminals" (servers).
    ```ini
    # inventory.ini
    [community_terminals]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    # [other_groups]
    # another_server.example.com
    ```
    For local testing, `localhost` with `ansible_connection=local` is sufficient.

3.  **Customize Morale Messages (Optional)**:
    Edit `vars/morale_messages.yml` to add your own unique messages.
    ```yaml
    # vars/morale_messages.yml
    morale_messages:
      - "Remember, even in the darkest void, a single byte of hope can illuminate the path!"
      - "Your resilience is stronger than any temporal anomaly. Keep coding, survivor!"
      # ... add more ...
    ```

4.  **Run the playbook**:
    ```bash
    ansible-playbook -i inventory.ini broadcast_morale.yml
    ```

    To target a specific file instead of `/etc/motd`, you can pass the `morale_target_file` variable:
    ```bash
    ansible-playbook -i inventory.ini broadcast_morale.yml -e "morale_target_file=/opt/community_board.txt"
    ```

5.  **Verify**:
    Log in to one of your target servers and check `/etc/motd` (or your custom file) to see the new morale message.

## Testing

To run the self-contained, deterministic tests for this utility:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_broadcast_morale.yml
```

This test playbook verifies that the random message selection logic works correctly and that a message is successfully chosen from the `morale_messages` list. It does not modify any system files.
