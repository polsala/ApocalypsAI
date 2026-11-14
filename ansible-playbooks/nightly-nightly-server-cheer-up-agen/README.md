# Nightly Server Cheer-Up Agent

This Ansible playbook deploys a whimsical 'cheer-up' agent to your servers. It can install `cowsay` and `fortune-mod` packages, configure a login script to display random messages, and optionally deploy custom ASCII art.

## Features

-   **Whimsical Login Messages**: Displays a random fortune message using `cowsay` upon SSH login.
-   **Custom ASCII Art**: Optionally deploys a custom ASCII art file to be displayed.
-   **Configurable**: Easily enable/disable features and customize paths via Ansible variables.

## Usage

1.  **Inventory**: Update `src/inventory.ini` with your target servers.
    ```ini
    [servers]
    server1.example.com
    server2.example.com

    [all:vars]
    ansible_user=your_ssh_user
    ansible_ssh_private_key_file=~/.ssh/id_rsa
    ```

2.  **Configuration**: Review and modify variables in `src/vars/main.yml`.
    ```yaml
    # Default variables for the Nightly Server Cheer-Up Agent
    cheer_up_enable_cowsay: true
    cheer_up_enable_fortune: true
    cheer_up_motd_path: "/etc/profile.d/nightly_cheer.sh" # Path for the login script
    cheer_up_deploy_ascii_art: false # Set to true to deploy custom ASCII art
    cheer_up_custom_ascii_art_source: "files/my_whimsical_art.txt" # Source path for ASCII art (relative to playbook)
    cheer_up_custom_ascii_art_path: "/usr/local/share/nightly_ascii_art.txt" # Destination path on target server
    ```

3.  **Custom ASCII Art (Optional)**: If `cheer_up_deploy_ascii_art` is `true`, place your ASCII art file at `src/files/my_whimsical_art.txt` (or update `cheer_up_custom_ascii_art_source`). An example is provided.

4.  **Run the Playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/cheer_up.yml
    ```

    This will connect to your servers, install the necessary packages (if enabled), and deploy the login script and optional ASCII art.

## Testing

To run the tests, use the following command:

```bash
ansible-playbook -i tests/inventory.ini tests/test_cheer_up.yml
```

The tests are designed to be deterministic and offline, using mock variables to simulate the expected state of a target host after the playbook has run.
