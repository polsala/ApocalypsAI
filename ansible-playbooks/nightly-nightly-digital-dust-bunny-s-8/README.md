# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps you keep your servers tidy by identifying and optionally cleaning up "digital dust bunnies" – old, unused, or small files that accumulate over time.

## Features

*   **Configurable Paths**: Specify which directories to scan for dust bunnies.
*   **Age and Size Thresholds**: Define what constitutes a "dust bunny" based on its last modification time and file size.
*   **Actions**: Choose to merely `report` on found dust bunnies, `delete` them, or `archive` them to a specified directory.
*   **Whimsical Naming**: Because even server maintenance can be fun!

## Usage

1.  **Inventory**: Prepare an Ansible inventory file (`inventory.ini`) listing the target servers.
    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```
    A minimal `src/inventory.ini` is provided for local testing.

2.  **Configuration**: Adjust the variables in `src/vars/main.yml` to suit your needs.

    ```yaml
    ---
    # Configuration for the Digital Dust Bunny Sweeper
    dust_bunny_paths:
      - "/tmp"
      - "/var/log/old" # Example path, adjust as needed
      - "/home/{{ ansible_user }}/.cache" # User-specific cache
    dust_bunny_age_days: 30 # Files older than this many days
    dust_bunny_min_size_kb: 0 # Minimum size in KB (e.g., 0 for any size, 1 for >1KB)
    dust_bunny_max_size_kb: 1024 # Maximum size in KB (e.g., 1024 for files up to 1MB)
    dust_bunny_action: "report" # Options: "report", "delete", "archive"
    dust_bunny_archive_dir: "/var/dust_bunny_archive" # Where to move files if action is "archive"
    ```

3.  **Run the Playbook**:

    *   **Report Only (Safe Mode)**: This is the default and recommended first step. It will only list files that match your criteria.
        ```bash
        ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "dust_bunny_action=report"
        ```

    *   **Delete Dust Bunnies (Use with Caution!)**:
        ```bash
        ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "dust_bunny_action=delete"
        ```
        **Always run with `--check --diff` first to see what would be deleted!**
        ```bash
        ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "dust_bunny_action=delete" --check --diff
        ```

    *   **Archive Dust Bunnies**:
        ```bash
        ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "dust_bunny_action=archive"
        ```
        This will move files to the `dust_bunny_archive_dir` specified in `vars/main.yml`.
        Again, use `--check --diff` first.

## Requirements

*   Ansible (core modules only, no special collections needed beyond what's typically included).
*   Target hosts must be accessible via SSH and have Python installed.
*   `become: yes` is used, so appropriate sudo/privilege escalation setup is required on target hosts for paths requiring root access.

## Testing

To run the included tests, execute the test playbook:

```bash
ansible-playbook -i src/inventory.ini tests/test_dust_bunny_sweeper.yml
```

This will run a series of tests that mock the `find` module's output and verify the playbook's logic in various scenarios (no dust bunnies, dust bunnies found, different actions in check mode).
