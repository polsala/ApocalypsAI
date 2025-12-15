# Nightly Digital Dust Bunny Sweeper

## Summary
This Ansible playbook helps you keep your servers tidy by identifying and removing old, unused files and directories, much like sweeping away digital dust bunnies. It's designed for system hygiene, freeing up disk space, and reducing clutter across your infrastructure.

## Features
*   **Configurable Scan Paths**: Specify which directories to scan for old files.
*   **Age Threshold**: Define how old a file or directory must be before it's considered a "dust bunny" (based on access time).
*   **Dry Run Mode**: Safely preview what would be deleted without making any changes.
*   **Detailed Reporting**: Get a summary of identified and (optionally) removed items.

## Prerequisites
*   Ansible installed on your control machine.
*   SSH access to your target servers from the control machine.
*   Python installed on target servers (required for Ansible modules).

## Usage

### 1. Inventory
Create an `inventory.ini` file listing your target servers.

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com

[all:vars]
ansible_user=your_ssh_user
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

### 2. Configuration Variables
Edit `vars/main.yml` to define your scan paths and age threshold.

```yaml
# vars/main.yml
---
# List of paths to scan for old files/directories
scan_paths:
  - /tmp
  - /var/log/old_archives
  - /opt/temp_builds

# Age threshold in days. Files/directories older than this will be considered dust bunnies.
age_threshold_days: 30

# Set to 'true' for a dry run (only reports, no deletion), 'false' to actually delete.
dry_run: true
```

### 3. Run the Playbook

#### Dry Run (Recommended First)
To see what would be swept without making any changes:
```bash
ansible-playbook -i inventory.ini dust_bunny_sweeper.yml -e "dry_run=true"
```

#### Actual Sweeping
To actually remove the identified dust bunnies:
```bash
ansible-playbook -i inventory.ini dust_bunny_sweeper.yml -e "dry_run=false"
```

### Example Output (Dry Run)
```
PLAY [Sweep Digital Dust Bunnies] **********************************************

TASK [Gathering Facts] *********************************************************
ok: [web1.example.com]
ok: [db1.example.com]

TASK [Find old files and directories] ******************************************
ok: [web1.example.com] => {
    "msg": "Found 2 dust bunnies on web1.example.com:\n- /tmp/old_log.txt (accessed 60 days ago)\n- /tmp/old_dir (accessed 45 days ago)"
}
ok: [db1.example.com] => {
    "msg": "Found 1 dust bunny on db1.example.com:\n- /var/log/old_archives/backup.tar.gz (accessed 90 days ago)"
}

TASK [Report on identified dust bunnies (Dry Run)] *****************************
ok: [web1.example.com] => {
    "msg": "DRY RUN: Would remove 2 items on web1.example.com.\nIdentified dust bunnies:\n- /tmp/old_log.txt (accessed 60 days ago)\n- /tmp/old_dir (accessed 45 days ago)"
}
ok: [db1.example.com] => {
    "msg": "DRY RUN: Would remove 1 item on db1.example.com.\nIdentified dust bunnies:\n- /var/log/old_archives/backup.tar.gz (accessed 90 days ago)"
}

PLAY RECAP *********************************************************************
web1.example.com           : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
db1.example.com            : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Testing
The `tests/` directory contains a setup for local testing using `localhost`.
1.  Ensure Ansible is installed.
2.  Navigate to the utility's root directory.
3.  Run the test playbook:
    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
    ```
This will create temporary files, run the sweeper in dry-run and actual modes, and then verify the results.
