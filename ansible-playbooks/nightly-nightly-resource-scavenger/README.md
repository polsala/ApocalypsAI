# Nightly Resource Scavenger

This Ansible playbook, the 'Nightly Resource Scavenger', helps you identify and report on potentially forgotten or excessively large files and directories across your remote servers. In the post-apocalyptic digital landscape, managing your disk space and identifying stale data is crucial for survival. This utility acts as your digital scavenger, unearthing hidden 'resources' that might need attention.

## Features

*   Scans specified paths for files exceeding a configurable size threshold.
*   Identifies files older than a specified age threshold.
*   Reports on the top-level disk usage of scanned directories.
*   Generates a human-readable report detailing the findings.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions.
*   Python on target servers (for Ansible modules).

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file (or use an existing one) listing your target servers.

    ```ini
    [wasteland_servers]
    server1.example.com
    server2.example.com
    ```

2.  **Configure Scavenger Settings**: Edit `vars/scavenger_config.yml` to define the paths to scan, file size thresholds, and age thresholds.

    ```yaml
    # vars/scavenger_config.yml
    scavenger_paths:
      - /var/log
      - /opt
      - /home

    scavenger_min_file_size_mb: 10 # Minimum file size in MB to report
    scavenger_max_file_age_days: 30 # Maximum age in days for files to be considered 'old'
    scavenger_report_path: "/tmp/scavenger_report_{{ ansible_hostname }}.txt"
    ```

3.  **Run the playbook**: Execute the playbook from your control machine.

    ```bash
    ansible-playbook -i inventory.ini src/scavenge_resources.yml
    ```

    The report will be generated on each target server at the path specified by `scavenger_report_path`.

## Example Report Output

```
ApocalypsAI Nightly Resource Scavenger Report for server1.example.com (2023-10-27T10:30:00.123456)

Discovered Digital Relics (Files > 10MB or older than 30 days):
- Path: /var/log/old_archive.tar.gz
  Size: 15.23 MB
  Modification Time: 2023-08-01 12:00:00
- Path: /opt/backup/database_dump.sql
  Size: 102.50 MB
  Modification Time: 2023-10-20 08:15:00

Top-Level Directory Sizes in Scanned Paths:
- Path: /var/log
  Size: 2.5G
- Path: /opt
  Size: 500M
- Path: /home
  Size: 10G

---
End of Report. Stay vigilant, survivor.
```
