# Nightly Digital Dust-Bunny Sweeper

An Ansible playbook to whimsically sweep away digital dust bunnies (temporary files, old logs, orphaned packages) from your servers, ensuring pristine post-apocalyptic system hygiene.

## Purpose

In the post-apocalyptic digital landscape, even servers accumulate "digital dust" – temporary files, old logs, and forgotten packages that can clutter the system and consume precious resources. This playbook acts as your diligent digital janitor, tidying up these forgotten corners with a touch of whimsy.

It's designed to be run periodically to maintain system cleanliness and report on its findings.

## Features

*   **Temporary File Cleanup**: Removes old files from common temporary directories (`/tmp`, `/var/tmp`).
*   **Log File Pruning**: Deletes old compressed log files (`.gz`, `.xz`, `.bz2`) to free up disk space.
*   **Orphaned Package Removal**: Identifies and removes packages that are no longer needed (Debian/Ubuntu specific).
*   **Whimsical Report Generation**: Creates a summary report of the cleanup activities, detailing what was swept away.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions (e.g., `sudo` access for cleanup tasks).

### Inventory

Create an `inventory.ini` file (or use the provided example) listing your target servers:

```ini
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com
```

### Configuration

Customize the cleanup targets and ages in `src/vars/cleanup_targets.yml`:

```yaml
---
cleanup_paths:
  - path: /tmp
    age: 7d # files older than 7 days
  - path: /var/tmp
    age: 30d # files older than 30 days
  - path: /var/log
    patterns:
      - "*.gz"
      - "*.log.[0-9]"
    age: 30d # logs older than 30 days
```

### Running the Playbook

To perform a dry run (recommended first!):

```bash
ansible-playbook -i src/inventory.ini src/dust_sweeper.yml --check
```

To execute the cleanup:

```bash
ansible-playbook -i src/inventory.ini src/dust_sweeper.yml
```

The playbook will generate a cleanup report in `reports/` directory on the control machine.

### Example Output (Report)

```
--- Digital Dust-Bunny Sweeper Report ---
Date: 2023-10-27 08:00:00 UTC

Server: web1.example.com
  🗑️ Swept away 12 files from /tmp (older than 7 days).
  🗑️ Cleared 3 old log archives from /var/log (older than 30 days).
  📦 Found 0 orphaned packages. System is sparkling!

Server: db1.example.com
  🗑️ Swept away 0 files from /tmp. A surprisingly clean corner!
  🗑️ Cleared 5 old log archives from /var/log.
  📦 Found 2 orphaned packages. Consider running 'apt autoremove' manually if desired.

--- End of Report ---
```

## Testing

The playbook includes a self-contained test suite using Ansible's `check_mode` and `assert` modules.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_sweeper.yml
```

This will:
1.  Create dummy "dust bunnies" on `localhost`.
2.  Run the `dust_sweeper.yml` playbook in `check_mode` against `localhost`.
3.  Assert that the expected changes *would* be made.
4.  Clean up the dummy files.
