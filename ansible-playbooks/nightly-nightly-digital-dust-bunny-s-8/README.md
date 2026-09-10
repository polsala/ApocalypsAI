# Nightly Digital Dust Bunny Sweeper

## Summary
This Ansible playbook, affectionately known as the "Digital Dust Bunny Sweeper," helps maintain a tidy and efficient server environment by automatically identifying and removing old, temporary files, logs, and cache entries that accumulate over time.

## How it Works
The playbook iterates through a configurable list of paths and age thresholds. For each specified path, it finds files older than the defined age and removes them. This helps reclaim disk space and prevent performance degradation caused by digital clutter.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access to your target servers (or `localhost` for local cleanup).
- Python installed on target servers (required for Ansible modules).

### 1. Inventory Configuration (`src/inventory.ini`)
Define the hosts you want to clean up. For local execution, `localhost` is sufficient.

```ini
[servers]
localhost ansible_connection=local
# Add your remote servers here:
# webservers
#   server1.example.com
#   server2.example.com
```

### 2. Cleanup Paths Configuration (`vars/cleanup_paths.yml`)
Specify the directories to scan and the age (in days) after which files should be considered "dust bunnies" and removed. You can define multiple targets.

```yaml
# Define the paths to sweep for digital dust bunnies and their maximum allowed age.
# Files older than 'age_days' in 'path' will be removed.
cleanup_targets:
  - path: "/tmp/old_temp_files" # General temporary files
    age_days: 1
  - path: "/var/log/app_archives" # Archived application logs
    age_days: 7
  - path: "/home/{{ ansible_user }}/.cache/downloads" # User-specific download caches
    age_days: 30
```

### 3. Running the Playbook
Execute the playbook from your control machine:

```bash
ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml
```

To perform a dry run and see what *would* be removed without actually deleting anything, use the `--check` flag:

```bash
ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml --check
```

## Testing
To ensure the Digital Dust Bunny Sweeper works as expected, a dedicated test playbook is provided. It creates temporary files, runs the main playbook in check mode and then for real, and verifies the cleanup.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_bunny_sweeper.yml
```

This will create a temporary directory, populate it with old and new files, run the sweeper, and assert that only the old files are removed, then clean up the test directory.
