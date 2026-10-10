# Nightly Temporal Echo Purifier

## Summary

This Ansible playbook, `nightly-temporal-echo-purifier`, is designed to cleanse your servers of accumulated digital detritus, or "temporal echoes." It targets common areas where temporary files, old logs, and orphaned Docker resources tend to linger, ensuring a pristine and efficient operational environment.

## Features

*   **Temporary File Cleanup:** Removes old files and directories from `/tmp` and `/var/tmp` based on a configurable age threshold.
*   **Stale Log Purge:** Deletes log files older than a specified number of days from `/var/log`, with an exclusion list for critical system logs.
*   **Docker System Prune:** Conditionally executes `docker system prune` to remove unused Docker images, containers, volumes, and networks, if the Docker service is detected as running.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   The `community.docker` collection installed (if Docker cleanup is desired): `ansible-galaxy collection install community.docker`.
*   SSH access to your target servers with appropriate permissions (e.g., `sudo` access for cleanup tasks).

### Files

*   `src/echo_purifier.yml`: The main Ansible playbook.
*   `src/inventory.ini`: A sample inventory file. Modify this to list your target servers.
*   `src/vars/cleanup_config.yml`: Configuration variables for cleanup thresholds and exclusions.

### Configuration (`src/vars/cleanup_config.yml`)

```yaml
---
# Number of days after which files in /tmp and /var/tmp should be removed
cleanup_tmp_days: 7

# Number of days after which log files in /var/log should be removed
cleanup_log_days: 30

# List of log files (base names) to exclude from cleanup in /var/log
cleanup_log_exclude:
  - auth.log
  - syslog
  - kern.log
  - dmesg
  - bootstrap.log
  - lastlog
  - wtmp
  - btmp
```

### Running the Playbook

1.  **Update Inventory:** Edit `src/inventory.ini` to include your target hosts.
    ```ini
    [servers]
    your_server_ip_or_hostname
    another_server_ip_or_hostname
    ```

2.  **Run the Playbook:** Execute the playbook from the utility's root directory:
    ```bash
    ansible-playbook -i src/inventory.ini src/echo_purifier.yml --ask-become-pass
    ```
    (Use `--ask-become-pass` if your user requires a password for `sudo`.)

### Dry Run

It's highly recommended to perform a dry run first to see what changes would be made without actually executing them:

```bash
ansible-playbook -i src/inventory.ini src/echo_purifier.yml --check --diff --ask-become-pass
```

## Automated Tests

The `tests/test_echo_purifier.yml` playbook provides a self-contained, deterministic, and offline test suite for the core cleanup logic. It simulates an environment with old files and logs, runs the purifier, and asserts that the expected files are removed.

### Running Tests

From the utility's root directory:

```bash
ansible-playbook -i src/inventory.ini tests/test_echo_purifier.yml
```

**Note:** The test playbook uses `localhost` and creates temporary directories to avoid affecting your actual system. It does not execute `docker system prune` but verifies the task's presence and conditions.
