# Nightly Log Rotate & Archive

## Overview

This Ansible playbook rotates the system logs in `/var/log`, compresses logs older than a configurable number of days, and uploads the archived logs to a remote backup server via `rsync`.

## Features

- Safe rotation using `logrotate` configuration.
- Compression of rotated logs with `gzip`.
- Optional remote backup via `rsync` (SSH).
- Idempotent – safe to run repeatedly.

## Requirements

- Ansible 2.9+ installed on the control node.
- Target hosts must have `logrotate`, `gzip`, and `rsync` available.
- SSH access to the remote backup server (if backup is enabled).

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `logrotate_path` | `/etc/logrotate.d` | Directory where logrotate config files are placed. |
| `log_files` | `["/var/log/*.log"]` | List of log file glob patterns to rotate. |
| `rotate_days` | `7` | Keep rotated logs for this many days before deletion. |
| `backup_enabled` | `false` | Set to `true` to enable remote backup. |
| `backup_destination` | `"backup@example.com:/backups/logs"` | Remote rsync destination (user@host:/path). |
| `backup_user` | `"backup"` | SSH user for remote backup. |

## Usage

```bash
ansible-playbook -i inventory.ini src/log_rotate.yml \
  -e "logrotate_path=/etc/logrotate.d log_files=['/var/log/syslog','/var/log/auth.log'] rotate_days=14 backup_enabled=true backup_destination='backup@example.com:/backups/logs'"
```

## Testing

Run the included test playbook with:

```bash
ansible-playbook -i localhost, tests/test_log_rotate.yml
```

The test uses mock variables and does not modify real system logs.
