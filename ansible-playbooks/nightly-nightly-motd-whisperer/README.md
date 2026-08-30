# Nightly MOTD Whisperer

An Ansible playbook to propagate whimsical ApocalypsAI-themed "whispers" as messages of the day (MOTD) across your managed servers. Keep your system administrators and users entertained with cryptic, yet oddly comforting, messages from the void.

## Features

*   **Whimsical Messages**: Delivers a random, pre-defined ApocalypsAI-themed message to `/etc/motd`.
*   **Easy Customization**: Add or modify messages in `vars/motd_messages.yml`.
*   **Idempotent**: Runs without making unnecessary changes if the MOTD is already one of the expected whispers.
*   **Ansible-Native**: Leverages standard Ansible modules for broad compatibility.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers (if not `localhost`).
*   `sudo` privileges on target servers for updating `/etc/motd`.

## Usage

1.  **Clone the repository (or copy this utility's folder):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-motd-whisperer
    ```

2.  **Review and customize the inventory:**
    Edit `src/inventory.ini` to include your target servers. For local testing, `localhost` is pre-configured.

    ```ini
    # src/inventory.ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

3.  **Customize your whispers (optional):**
    Edit `src/vars/motd_messages.yml` to add, remove, or modify the list of messages.

    ```yaml
    # src/vars/motd_messages.yml
    motd_messages:
      - "The void whispers greetings, survivor. Your systems are online."
      - "Another cycle begins. May your packets flow freely through the temporal rifts."
      # ... more messages
    ```

4.  **Run the playbook:**
    Execute the playbook from the `nightly-motd-whisperer` directory:

    ```bash
    ansible-playbook -i src/inventory.ini src/motd_whisperer.yml
    ```
    This will connect to your `[servers]` group, select a random message, and update `/etc/motd` on each.

## Testing

To run the automated tests for this utility:

1.  Ensure you have Ansible installed.
2.  Navigate to the utility's directory:
    ```bash
    cd ApocalypsAI/ansible-playbooks/nightly-motd-whisperer
    ```
3.  Execute the test playbook:
    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_motd_whisperer.yml
    ```
    The test playbook will:
    *   Run the main `motd_whisperer.yml` playbook in `check_mode`.
    *   Run the main playbook for real on `localhost`.
    *   Read the content of `/etc/motd`.
    *   Assert that the content is one of the predefined messages from `src/vars/motd_messages.yml`.

## Example Output (after running playbook)

```
$ ssh localhost
The void whispers greetings, survivor. Your systems are online.
Last login: ...
```
(The message will vary based on random selection)
