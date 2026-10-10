# Nightly Resource Goblin Tamer

## Overview
The `nightly-resource-goblin-tamer` is an Ansible playbook designed to help you identify and manage system resource hogs, whimsically referred to as "resource goblins." It scans your Linux servers for excessive disk usage, large files, high memory consumption, and active CPU processes, then provides a comprehensive report. Optionally, it can perform basic cleanup actions to free up resources.

## Features
- **Disk Usage Report**: Shows overall disk space consumption.
- **Large File Detection**: Identifies files exceeding a configurable size threshold.
- **Memory Usage Report**: Displays current memory and swap utilization.
- **CPU Usage Report**: Provides an overview of CPU activity.
- **Optional Cleanup**: Can clean `apt` caches and vacuum `journalctl` logs based on configuration.

## Prerequisites
- **Ansible**: Ensure Ansible is installed on your control machine (where you run the playbook).
- **SSH Access**: The target servers must be accessible via SSH from the control machine.
- **Sudo Privileges**: The playbook requires `become: true` (sudo) to perform system checks and cleanup actions.

## Usage

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-resource-goblin-tamer
    ```

2.  **Configure your inventory**: Edit `src/inventory.ini` to list your target servers. For local execution, `localhost` is pre-configured.
    ```ini
    # src/inventory.ini
    [servers]
    localhost ansible_connection=local
    # my_server_1 ansible_host=192.168.1.10 ansible_user=your_user
    # my_server_2 ansible_host=server.example.com ansible_user=your_user
    ```

3.  **Adjust variables (optional)**: Modify `src/vars/main.yml` to customize thresholds and enable/disable cleanup.
    ```yaml
    # src/vars/main.yml
    cleanup_enabled: false # Set to true to enable cleanup tasks (apt autoclean, journalctl vacuum)
    large_file_threshold_mb: 100 # Files larger than this will be reported (in MB)
    log_cleanup_size_mb: 50 # Max size for journalctl vacuum (in MB)
    ```

4.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/tame_goblins.yml --ask-become-pass
    # Or, if using SSH keys with agent forwarding:
    # ansible-playbook -i src/inventory.ini src/tame_goblins.yml -b
    ```
    The `--ask-become-pass` flag will prompt you for the sudo password on the target machines.

## Output
The playbook will print detailed reports to your console, including disk usage, a list of large files, memory statistics, and CPU load. If `cleanup_enabled` is set to `true`, it will also report on the cleanup actions performed.

## Example Output (abbreviated)
```
PLAY [Tame Resource Goblins] ***************************************************

TASK [Gather system facts] *****************************************************
ok: [localhost]

TASK [Check Disk Usage] ********************************************************
ok: [localhost]

TASK [Report Disk Usage] *******************************************************
ok: [localhost] => {
    "msg": "---
          --- Disk Usage Report ---
          Filesystem      Size  Used Avail Use% Mounted on
          /dev/sda1        20G   18G  1.0G  95% /
          tmpfs           3.9G     0  3.9G   0% /dev/shm"
}

TASK [Find Large Files] ********************************************************
ok: [localhost]

TASK [Report Large Files ( >100MB)] *******************************************
ok: [localhost] => {
    "msg": "---
          --- Large Files Report (>100MB) ---
          150M /var/log/big_log_file.log
          120M /opt/another_big_file.data"
}

...

PLAY RECAP *********************************************************************
localhost                  : ok=8    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Testing
To run the automated tests, navigate to the utility's root directory and execute:
```bash
ansible-playbook -i src/inventory.ini tests/test_tame_goblins.yml
```
These tests use mocked command outputs to ensure the playbook's reporting logic functions correctly without making actual system changes.
