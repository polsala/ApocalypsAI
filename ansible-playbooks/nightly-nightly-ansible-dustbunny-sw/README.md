# Nightly Ansible Digital Dustbunny Sweeper

## Summary
This Ansible playbook, the "Digital Dustbunny Sweeper," is designed to whimsically yet effectively clean up remote servers by identifying and managing temporary files, old logs, and other digital clutter. It helps maintain system hygiene, free up disk space, and ensures your servers remain spick and span.

## How it Works
1.  **Quarantine Setup**: Ensures a designated `dustbunny_quarantine` directory exists on the target servers.
2.  **Temporary File Deletion**: Scans specified paths for files matching configurable patterns (e.g., `*.tmp`, `*.bak`, `~*`) that are older than a defined age, and deletes them.
3.  **Old Log Archiving**: Identifies log files (e.g., `*.log`, `*.gz`) older than a certain age and moves them to the `dustbunny_quarantine` directory, appending a timestamp to their names for easy identification.
4.  **Report Generation**: Creates a `dustbunny_report.txt` file on each target server, detailing which files were deleted and which were archived, providing a whimsical summary of the cleanup operation.

## Usage

1.  **Inventory**: Update the `src/inventory.ini` file with the hosts you wish to clean. For local testing, `localhost` is pre-configured.
    ```ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

2.  **Configuration**: Review and adjust the variables in `vars/main.yml` to customize scan paths, file patterns, ages for deletion/archiving, and the quarantine/report locations.
    ```yaml
    # Example vars/main.yml snippet
    dustbunny_scan_paths:
      - /tmp
      - /var/log
    dustbunny_temp_patterns:
      - '*.tmp'
      - '*.bak'
    dustbunny_temp_age: '7d'
    dustbunny_log_age: '30d'
    dustbunny_quarantine_path: /var/lib/dustbunny_quarantine
    dustbunny_report_path: /var/log/dustbunny_report.txt
    ```

3.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i src/inventory.ini src/dustbunny_sweeper.yml
    ```
    If you need to run it with elevated privileges (e.g., for cleaning `/var/log` or `/tmp`), add `--become`:
    ```bash
    ansible-playbook -i src/inventory.ini src/dustbunny_sweeper.yml --become
    ```

## Example Report Output (`/var/log/dustbunny_report.txt`)
```
Digital Dustbunny Sweeper Report - 2023-10-27T10:30:00Z

Greetings, my-server-hostname!

Your friendly neighborhood ApocalypsAI Dustbunny Sweeper has been hard at work, tidying up the digital nooks and crannies of your system.

---
DELETED TEMPORARY FILES:
- /tmp/old_cache.tmp
- /var/log/app.log.bak

---
ARCHIVED OLD LOGS/MISPLACED FILES (moved to /var/lib/dustbunny_quarantine):
- /var/log/syslog.log
- /var/log/auth.log

---
May your system run smoothly and free of digital clutter!
```

## Testing
To run the automated tests for this utility, use the provided test playbook:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dustbunny_sweeper.yml --become
```
This will set up a temporary environment, run the sweeper, and verify its actions.
