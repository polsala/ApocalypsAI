# Nightly Ansible Digital Pet Keeper

## Summary
This Ansible playbook acts as a diligent 'Digital Pet Keeper', ensuring that a specified critical background process (your 'digital pet') is always running, correctly configured, and its environment is kept tidy. It's designed for maintaining the health and happiness of any essential service or application component on your servers.

## Features
- **Home Sweet Home**: Ensures the digital pet's working directory exists with correct permissions.
- **Nourishment**: Deploys a templated configuration file, ensuring your pet is well-fed with the right settings.
- **Comfort & Care**: Manages the digital pet's systemd service, ensuring it's enabled and running.
- **Litter Box Cleanup**: Periodically prunes old log files to keep the pet's environment clean and prevent disk bloat.
- **Mood Report**: Provides a whimsical status update on your digital pet's current state.

## Prerequisites
- Ansible installed on your control machine.
- SSH access to your target servers with `sudo` privileges.
- Python 3 on target servers (Ansible's default).

## Usage
1.  **Clone the repository** (or copy this utility's folder).
2.  **Navigate** into the `nightly-ansible-digital-pet-keeper` directory.
3.  **Configure your inventory**: Edit `src/inventory.ini` to list your target hosts.
    ```ini
    [digital_pets]
    your_server_ip_or_hostname
    ```
4.  **Define your Digital Pet**: Modify `src/vars/pet_config.yml` with your pet's details.
    ```yaml
    pet_name: "LogGobbler"
    pet_service_name: "loggobbler"
    pet_working_dir: "/opt/loggobbler"
    pet_config_path: "/etc/loggobbler/config.ini"
    pet_log_dir: "/var/log/loggobbler"
    pet_log_retention_days: 7
    pet_command: "/usr/bin/loggobbler --config {{ pet_config_path }}"
    pet_user: "loggobbler_user"
    pet_group: "loggobbler_group"
    ```
5.  **Customize Templates (Optional)**: Adjust `src/templates/pet_service.j2` (for systemd) and `src/templates/pet_config_file.j2` to match your specific application's needs.
6.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml --ask-become-pass
    ```
    (Use `--ask-become-pass` if your sudo user requires a password).

## Example Output
```
PLAY [Ensure Digital Pet is Happy and Healthy] *********************************

TASK [Gathering Facts] *********************************************************
ok: [your_server_ip_or_hostname]

TASK [Ensure Digital Pet's home directory exists] ******************************
changed: [your_server_ip_or_hostname]

TASK [Deploy Digital Pet's configuration file] *********************************
changed: [your_server_ip_or_hostname]

TASK [Deploy Digital Pet's systemd service file] *******************************
changed: [your_server_ip_or_hostname]

TASK [Ensure Digital Pet service is enabled and running] ***********************
changed: [your_server_ip_or_hostname]

TASK [Gather Digital Pet service status] ***************************************
ok: [your_server_ip_or_hostname]

TASK [Clean Digital Pet's litter box (old log files)] **************************
ok: [your_server_ip_or_hostname]

TASK [Remove old log files] ****************************************************
skipping: [your_server_ip_or_hostname] => (item={'path': '/var/log/loggobbler/old.log', 'size': 1024, 'mtime': 1678886400, 'atime': 1678886400, 'ctime': 1678886400, 'isdir': False, 'islnk': False, 'ischr': False, 'isfifo': False, 'isblk': False, 'issock': False, 'isreg': True, 'uid': 1000, 'gid': 1000, 'mode': '0644', 'dev': 2049, 'nlink': 1, 'inode': 12345, 'xattr': {}}) 

TASK [Report Digital Pet's current mood] ***************************************
ok: [your_server_ip_or_hostname] => {
    "msg": "The Digital Pet 'LogGobbler' is purring happily!"
}

PLAY RECAP *********************************************************************
your_server_ip_or_hostname : ok=8    changed=4    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

## Testing
To run the included tests, navigate to the utility's root directory and execute:
```bash
ansible-playbook -i tests/inventory_test.ini tests/test_playbook.yml
```
These tests are designed to be deterministic and offline, primarily verifying the correct rendering of templates and the logical parameters passed to modules, rather than actual system modifications.
