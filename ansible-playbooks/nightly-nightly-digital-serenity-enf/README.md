# Nightly Digital Serenity Enforcer

## Summary
This Ansible playbook, the "Digital Serenity Enforcer," is designed to bring a sense of calm and order to your digital infrastructure. It automates the process of stopping non-essential services, clearing out digital detritus (temporary files), and ensuring proper log rotation to maintain system hygiene and reduce unnecessary resource consumption.

In the post-apocalyptic landscape, every byte and CPU cycle counts. This utility helps keep your systems lean, quiet, and focused on critical tasks, preventing digital clutter from becoming a source of chaos.

## How it Works
The playbook performs the following actions on target hosts:
1.  **Stops Non-Essential Services**: Shuts down services specified in the configuration that are not critical for core operations, freeing up resources.
2.  **Cleans Temporary Files**: Removes files and directories from common temporary locations, reducing disk usage and potential security risks.
3.  **Configures & Forces Log Rotation**: Ensures that system logs are properly rotated and compressed, preventing them from consuming excessive disk space and making them easier to manage.

## Usage
1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target hosts with `sudo` privileges.

2.  **Inventory**: Create an `inventory.ini` file (or modify the provided example) listing your target hosts under the `[serenity_targets]` group.

    ```ini
    [serenity_targets]
    localhost ansible_connection=local
    # server1.example.com ansible_user=your_user
    # server2.example.com ansible_user=your_user
    ```

3.  **Configuration**: Review and customize the `vars/serenity_config.yml` file to define which services to stop, which paths to clean, and log rotation settings.

    ```yaml
    serenity_services_to_stop:
      - apache2
      - nginx
      - cups
      - modemmanager

    serenity_temp_paths_to_clean:
      - /tmp/*
      - /var/tmp/*
      - /var/log/*.old
      - /var/log/*.bak

    serenity_logrotate_config_path: /etc/logrotate.d/serenity_logs
    serenity_logrotate_rotate_count: 14
    serenity_logrotate_create_mode: '0600'
    serenity_logrotate_create_owner: 'root'
    serenity_logrotate_create_group: 'root'
    ```

4.  **Run the Playbook**:
    Execute the playbook using the `ansible-playbook` command:

    ```bash
    ansible-playbook -i src/inventory.ini src/serenity_enforcer.yml
    ```

    To perform a dry run without making any changes (highly recommended for testing!):

    ```bash
    ansible-playbook -i src/inventory.ini src/serenity_enforcer.yml --check
    ```

## Directory Structure
```
ansible-playbooks/nightly-digital-serenity-enforcer/
├── README.md
├── src/
│   ├── serenity_enforcer.yml
│   └── inventory.ini
├── vars/
│   └── serenity_config.yml
├── templates/
│   └── serenity_logrotate.j2
└── tests/
    └── test_serenity_enforcer.yml
```
