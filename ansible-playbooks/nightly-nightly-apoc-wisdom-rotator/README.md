# Nightly Apocalyptic Wisdom Rotator

An Ansible playbook to rotate "Apocalyptic Wisdom" messages on server login banners (MOTD) or user terminals, keeping spirits high in the wasteland. Because even after the end, a little encouragement goes a long way.

## Features

*   **Dynamic MOTD:** Updates the Message Of The Day (`/etc/motd`) with a randomly selected wisdom message.
*   **Customizable Wisdom:** Easily add or modify the pool of apocalyptic wisdom messages.
*   **Idempotent:** Runs safely without making unnecessary changes if the message is already present.

## Requirements

*   Ansible (version 2.9 or higher recommended)
*   SSH access to target hosts with appropriate permissions (e.g., `sudo` for `/etc/motd`).

## Usage

1.  **Define your inventory:**
    Create an `src/inventory.ini` file (or use an existing one) listing your target servers.

    ```ini
    [wasteland_servers]
    server1.example.com
    server2.example.com
    ```

2.  **Customize Wisdom Messages (Optional):**
    Edit `src/vars/wisdom_messages.yml` to add your own pearls of post-apocalyptic insight.

    ```yaml
    # src/vars/wisdom_messages.yml
    ---
    wisdom_messages:
      - "The sun may set on civilization, but it rises on new opportunities."
      - "Keep your wits sharp and your water clean. Survival is a mindset."
      - "Even in the ruins, beauty can be found. Look closer."
      - "A well-maintained tool is a loyal companion. Cherish your gear."
      - "Remember the past, but build for the future. The wasteland awaits your touch."
    ```

3.  **Run the Playbook:**
    Execute the playbook using `ansible-playbook`:

    ```bash
    ansible-playbook -i src/inventory.ini src/rotate_wisdom.yml --ask-become-pass
    ```
    (Use `--ask-become-pass` if `sudo` requires a password, or configure passwordless sudo.)

    To run in check mode (dry run) and see what changes *would* be made:
    ```bash
    ansible-playbook -i src/inventory.ini src/rotate_wisdom.yml --check --diff
    ```

## Customization

*   **Target File:** By default, the playbook updates `/etc/motd`. You can modify `src/rotate_wisdom.yml` to target a different file or even a user's `.bashrc` or `.zshrc` (though this would require more complex logic to append/replace lines).
*   **Message Source:** The `wisdom_messages.yml` file is the primary source. You can point to a different file or even fetch messages from an external API (though this would break the "offline" requirement for the utility itself, so keep it local for this version).

## Testing

The `tests/test_rotate_wisdom.yml` playbook provides a deterministic way to verify the playbook's logic without actual server interaction. It uses `check_mode` and overrides the random message selection to ensure the templating process works as expected.
