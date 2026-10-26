# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps you keep your digital infrastructure tidy by sweeping away "digital dust bunnies" – those pesky temporary files, old logs, and forgotten caches that accumulate over time. Think of it as a friendly, automated cleaning crew for your servers, ensuring a lean and efficient environment.

## Features

*   **Temporary File Cleanup**: Removes old files from common temporary directories (`/tmp`, `/var/tmp`).
*   **Log File Pruning**: Deletes or archives old log files based on age.
*   **User Cache Clearing**: Cleans out user-specific cache directories (if configured).
*   **Configurable**: Easily adjust the age threshold for files to be considered "dust bunnies" and the paths to clean.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target servers.

2.  **Inventory**:
    Update `src/inventory.ini` with your target hosts. For example:
    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```

3.  **Configuration**:
    Review and adjust variables in `src/vars/main.yml`:
    ```yaml
    ---
    # src/vars/main.yml
    dust_bunny_age_days: 30 # Files older than this will be considered dust bunnies
    paths_to_clean:
      - /tmp
      - /var/tmp
      - /var/log/old_app_logs # Example: specific application log directory
    ```

4.  **Run the Playbook**:
    Execute the playbook from the root of this utility's directory:
    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml
    ```
    To perform a dry run without making any changes:
    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml --check
    ```

## Automated Tests

The `tests/test_playbook.yml` playbook verifies the cleanup functionality by creating a temporary file and asserting its removal.

To run the tests:
```bash
ansible-playbook -i tests/inventory_test.ini tests/test_playbook.yml
```

## Contributing

Feel free to suggest new "dust bunny" locations or cleanup strategies!
