# Nightly Digital Dust Bunny Sweeper

## Summary
This Ansible playbook helps you tidy up your digital spaces by identifying and optionally removing "digital dust bunnies" – old, forgotten, or temporary files lurking in specified directories on your remote servers. Keep your systems sparkling clean and free from digital clutter!

## Features
-   **Scan for Old Files**: Configurable paths and age thresholds to find files that haven't been accessed or modified recently.
-   **Detailed Reporting**: Generates a human-readable report of all identified dust bunnies.
-   **Optional Cleanup**: Safely remove identified files after review, or just use it for reporting.
-   **Whimsical Theme**: Because even system maintenance can be a little fun!

## Prerequisites
-   Ansible installed on your control machine.
-   SSH access to your target servers with appropriate permissions.
-   Python on target servers (for Ansible modules).

## Usage

### 1. Inventory
Create an `src/inventory.ini` file (or use an existing one) listing your target servers.

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
```

### 2. Configuration
Edit `src/vars/main.yml` to define your scan paths, age threshold, and cleanup preference.

```yaml
# src/vars/main.yml
---
scan_paths:
  - /tmp
  - /var/log/old_archives
  - /home/*/downloads
age_threshold_days: 30 # Files older than 30 days are considered dust bunnies
cleanup_enabled: false # Set to true to actually delete files
# Path on the *control machine* where the report for each host will be saved.
local_report_dir: "./reports"
```

### 3. Run the Playbook

**To generate a report (recommended first step):**
```bash
ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "cleanup_enabled=false"
```
This will run the playbook and generate reports for each host in the `local_report_dir` on your control machine.

**To perform cleanup (use with caution!):**
```bash
ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "cleanup_enabled=true" --ask-become-pass
```
(Add `--ask-become-pass` if root privileges are needed for cleanup in certain paths).

## How it Works
1.  The playbook connects to your target servers.
2.  It uses the `find` module to locate files in `scan_paths` that are older than `age_threshold_days`.
3.  It collects the list of "dust bunnies" from each host.
4.  It generates a detailed report for each host, saved to the `local_report_dir` on your control machine.
5.  If `cleanup_enabled` is `true`, it uses the `file` module to remove the identified files.

## Testing
To run the tests, ensure you have Ansible installed and then execute:
```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
```
