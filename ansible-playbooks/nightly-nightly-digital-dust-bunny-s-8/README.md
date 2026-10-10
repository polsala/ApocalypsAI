# Nightly Digital Dust Bunny Sweeper

## Summary
This Ansible playbook helps you combat the insidious accumulation of "digital dust bunnies" – those old, temporary, and forgotten files that silently consume disk space and clutter your systems. It's designed to be a whimsical yet effective tool for maintaining digital hygiene across your infrastructure.

## What it Does
The playbook identifies and removes files and directories based on configurable criteria such as age, name patterns, and emptiness. It targets common locations where digital clutter tends to gather, helping to free up valuable disk space and improve system performance.

## How it Works
The main playbook `src/dust_bunny_sweeper.yml` orchestrates the cleanup by iterating through a list of defined `cleanup_targets` (from `src/vars/cleanup_targets.yml`). For each target, it includes `src/tasks/main.yml` which contains the core logic for finding and removing files and empty directories based on the specified criteria.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access to your target hosts (if not running locally).

### 1. Define Your Inventory
Create an `inventory.ini` file (or use an existing one) listing the hosts you want to clean.

```ini
[servers]
server1.example.com
server2.example.com

[local]
localhost ansible_connection=local
```

### 2. Configure Cleanup Targets
Edit `src/vars/cleanup_targets.yml` to specify the paths and criteria for what constitutes a "digital dust bunny."

```yaml
# src/vars/cleanup_targets.yml
cleanup_targets:
  - path: /tmp
    age_days: 7
    patterns:
      - "*.log"
      - "*.tmp"
    description: "Temporary files older than 7 days in /tmp"
  - path: "{{ ansible_env.HOME }}/Downloads"
    age_days: 30
    patterns:
      - "*.old"
      - "*.bak"
    description: "Old downloads and backup files in user's Downloads folder"
  - path: "{{ ansible_env.HOME }}/.cache"
    age_days: 60
    description: "Cache files older than 60 days in user's cache directory"
  - path: "/var/log"
    age_days: 14
    patterns:
      - "*.gz"
      - "*.1"
    description: "Archived logs in /var/log"
  - path: "/opt/old_projects"
    empty_dirs: true
    description: "Empty directories in /opt/old_projects"
```

### 3. Run the Sweeper
Execute the playbook using the `ansible-playbook` command:

```bash
ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml
```

**Important**: It's highly recommended to run in `check_mode` first to see what *would* be removed:

```bash
ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml --check --diff
```

This will show you a detailed report of files and directories that match the cleanup criteria without actually deleting them.

## Automated Tests

To run the tests, ensure you have Ansible installed. The tests create temporary files and directories on `localhost` and then verify the playbook correctly identifies and removes them.

```bash
ansible-playbook -i src/inventory.ini tests/test_dust_bunny_sweeper.yml
```

The `test_dust_bunny_sweeper.yml` playbook will:
1. Create a temporary directory.
2. Populate it with dummy "dust bunny" files and directories that match the cleanup criteria.
3. Run the core cleanup tasks (`src/tasks/main.yml`) against this temporary location with test-specific variables.
4. Verify that the dummy files/directories have been removed.
5. Clean up the temporary directory.
