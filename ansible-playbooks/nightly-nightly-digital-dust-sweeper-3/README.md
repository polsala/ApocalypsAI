# Nightly Digital Dust Bunny Sweeper

An Ansible playbook to sweep away digital dust bunnies (temporary files, old logs, forgotten caches) from remote servers.

## Overview

This playbook helps maintain server hygiene by identifying and removing old, unnecessary files from specified directories. It targets common locations for temporary files, logs, and caches, ensuring your systems stay lean and mean.

## Features

-   **Configurable Paths**: Easily define which directories to clean and what age threshold to apply.
-   **Pattern Matching**: Use glob patterns to target specific file types (e.g., `*.log`, `*.tmp`).
-   **Detailed Reporting**: Get a summary of what was swept away.

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

2.  **Configure cleanup paths**:
    Edit `src/vars/cleanup_paths.yml` to specify the directories, age thresholds (in days), and file patterns for cleanup.

    ```yaml
    # src/vars/cleanup_paths.yml
    cleanup_targets:
      - path: /tmp
        age_days: 7
        patterns: ["*"]
      - path: /var/log
        age_days: 30
        patterns: ["*.log", "*.gz"]
      - path: /var/cache/apt/archives # Example for Debian/Ubuntu
        age_days: 30
        patterns: ["*.deb"]
      - path: /home/*/Downloads # Wildcard for user home directories
        age_days: 60
        patterns: ["*"]
    ```

3.  **Run the playbook**:

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_sweeper.yml
    ```

    Add `--check` for a dry run, or `--diff` to see what changes would be made.

## Requirements

-   Ansible (version 2.9 or higher recommended)
-   SSH access to target servers with appropriate permissions for file deletion.

## Testing

To run the automated tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_sweeper.yml
```

The tests will create temporary files, run the cleanup playbook against them, and verify that only the "old" files are removed.
