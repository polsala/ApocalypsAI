# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps maintain system hygiene by identifying and removing old, temporary, or unused files across your servers. Think of it as a digital vacuum cleaner for your infrastructure, sweeping away the 'dust bunnies' that accumulate over time.

## Features

*   **Configurable Paths**: Specify which directories to scan for old files.
*   **Configurable Age**: Define how old a file must be to be considered a 'dust bunny' and eligible for removal.
*   **Idempotent**: Ensures target directories exist before scanning.
*   **Reporting**: Provides a summary of files found and removed.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers (if not running locally).
*   `become` (sudo/root) privileges on target servers for file management in system directories.

## Usage

1.  **Configure Inventory**: Edit `src/inventory.ini` to list your target servers. For local execution, `localhost` is pre-configured.

    ```ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

2.  **Configure Cleanup Settings**: Modify `vars/cleanup_config.yml` to define the paths to scan and the age threshold for removal.

    ```yaml
    ---
    cleanup_paths:
      - "/tmp/digital_dust"
      - "/var/log/archive"
      - "/var/cache/old_packages"
    cleanup_age_days: 30 # Files older than 30 days will be removed
    ```

3.  **Run the Playbook**: Execute the playbook from your control machine.

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml
    ```

    To run with a specific user (e.g., `ansible_user=youruser`) and prompt for sudo password:

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -u youruser --ask-become-pass
    ```

## Testing

To ensure the sweeper works as expected, a dedicated test playbook is provided. This test creates temporary files with varying ages and verifies that only the 'old' files are removed.

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
```

## Contributing

Feel free to suggest improvements or add more sophisticated cleanup rules. Let's keep our digital spaces sparkling clean!
