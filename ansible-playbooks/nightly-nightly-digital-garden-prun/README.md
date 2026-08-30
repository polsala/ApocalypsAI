# Nightly Digital Garden Pruner

## Summary
This Ansible playbook acts as your server's diligent gardener, pruning digital weeds (temporary files, old package caches) and providing a health report on your filesystem's 'garden'. It helps maintain system hygiene and free up valuable disk space.

## Features
- Cleans up specified temporary directories (e.g., `/tmp`, `/var/tmp`).
- Removes old package manager caches (APT for Debian/Ubuntu, YUM/DNF for RHEL/CentOS/Fedora).
- Generates a concise disk usage report for key partitions.

## Usage

1.  **Inventory**: Create an `inventory.ini` file listing the hosts you want to manage. Ensure Ansible can connect to these hosts (e.g., via SSH keys).

    ```ini
    [servers]
    server1.example.com
    server2.example.com
    ```

2.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/prune_garden.yml
    ```

3.  **Review Report**: After execution, a `garden_report.txt` will be generated in the `/tmp` directory on each target host (or a configurable path via `report_output_path` in `src/vars/main.yml`). This report will summarize disk usage.

## Configuration

Customize the `src/vars/main.yml` file to adjust cleanup parameters:

-   `temp_dirs_to_clean`: A list of directories where temporary files should be pruned.
-   `max_age_temp_files`: The maximum age (e.g., `1d`, `7d`, `30m`) for files in `temp_dirs_to_clean` before they are considered 'weeds' and removed. Files newer than this age will be preserved.
-   `report_output_path`: The directory on the remote host where the `garden_report.txt` will be saved.

## Requirements

-   Ansible (version 2.9 or higher recommended)
-   SSH access to target hosts
-   Sudo privileges on target hosts for cleanup tasks

## Testing

To ensure the Digital Garden Pruner works as expected without affecting your production systems, use the provided test playbook:

1.  **Navigate to the utility directory**:
    ```bash
    cd nightly-digital-garden-prun
    ```
2.  **Run the test playbook**:
    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_prune_garden.yml
    ```

The test playbook will:
-   Create a temporary 'mock garden' directory on the test host.
-   Populate it with dummy files of varying ages.
-   Execute the main `prune_garden.yml` playbook against this mock garden, overriding paths to target the test environment.
-   Verify that old files are removed and a report is generated with expected content.

**Mock rationale**: The tests create a controlled, isolated environment on the target host (or a local Docker container if `inventory_test.ini` points to `localhost`) to simulate the conditions for cleanup. This avoids modifying actual system files or caches during testing and ensures deterministic results. File ages are controlled by `touch` commands, and file presence/absence is checked with `stat` and `slurp` modules. The `apt` and `yum` cleanup tasks are allowed to run but are not directly asserted against mock files, as they operate on system-wide paths; their successful execution is implicitly tested by the playbook not failing.
