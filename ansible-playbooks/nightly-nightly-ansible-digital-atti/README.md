# Nightly Ansible Digital Attic Tidy

## Summary
This Ansible playbook, affectionately known as the "Digital Attic Tidy," helps you declutter your remote servers by sweeping away digital dust bunnies (old temporary files), archiving forgotten scrolls (aged log files), and clearing out cobwebbed corners (empty directories and stale package caches). It's designed to give your servers a fresh, airy feeling without disturbing anything important.

## Whimsical Purpose
Even the most robust servers can accumulate digital clutter over time. This utility ensures your systems remain spick and span, preventing performance degradation and freeing up precious disk space, all while maintaining a cheerful disposition. Think of it as a friendly robot butler tidying up your server's digital living space.

## Usage

### Prerequisites
*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions (sudo might be required for some cleanup tasks).

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
# ansible_ssh_private_key_file=~/.ssh/id_rsa
```

### 2. Configuration
Review and customize the `vars/tidy_config.yml` file. This file defines which paths to clean, how old files should be before removal, and whether to clear package caches.

```yaml
# vars/tidy_config.yml
---
# Paths to scan for old temporary files
temp_paths:
  - /tmp
  - /var/tmp

# Files older than this many days will be considered for removal
temp_file_age_days: 7

# Paths to scan for old log files (e.g., .log.gz, .log.1, etc.)
log_paths:
  - /var/log
  - /var/log/nginx # Example, adjust as needed
  - /var/log/apache2 # Example, adjust as needed

# Log files older than this many days will be considered for removal
log_file_age_days: 30

# Whether to clean package manager caches (e.g., apt clean for Debian/Ubuntu)
# Set to 'false' if you don't want this or if your OS doesn't support it.
enable_apt_clean: false
enable_yum_clean: false
enable_dnf_clean: false

# Paths to scan for empty directories to remove
empty_dir_paths:
  - /tmp
  - /var/tmp
  - /var/log # Be careful with this, ensure only truly empty subdirs are removed
```

### 3. Run the Playbook
Execute the playbook using the `ansible-playbook` command:

```bash
ansible-playbook -i inventory.ini src/attic_tidy.yml --ask-become-pass
```
(Use `--ask-become-pass` if your `ansible_user` requires a password for `sudo`.)

### Dry Run
It's highly recommended to perform a dry run first to see what changes would be made without actually executing them:

```bash
ansible-playbook -i inventory.ini src/attic_tidy.yml --check --diff --ask-become-pass
```

## How it Works
The playbook uses Ansible's `find` module to locate files and directories based on age and type, and then the `file` module to remove them. It also conditionally runs package manager cleanup commands based on your configuration and detected OS family.

## Automated Tests
The `tests/test_attic_tidy.yml` playbook creates a temporary test environment, runs the main `attic_tidy.yml` playbook, and then asserts that the expected files and directories have been cleaned up.
