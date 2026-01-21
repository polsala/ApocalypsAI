## Nightly Ansible Syslog Rotator

This utility provides an Ansible playbook to manage and rotate syslog files on remote systems. It helps prevent log disk space from filling up by automatically archiving and cleaning old log files.

### Features

*   Configurable log file rotation based on size and age.
*   Compression of rotated log files.
*   Customizable retention policies.
*   Idempotent execution.

### Usage

1.  **Inventory File (`inventory.ini`)**: Define your target hosts.
    ```ini
    [webservers]
    server1.example.com
    server2.example.com

    [dbservers]
    db1.example.com
    ```

2.  **Playbook (`syslog_rotator.yml`)**: This is the main playbook.

3.  **Variables (`vars/main.yml`)**: Customize rotation parameters.
    ```yaml
    # vars/main.yml
    log_files_to_rotate:
      - path: "/var/log/syslog"
        max_size: "100M"
        max_age: "7d"
        compress: true
      - path: "/var/log/auth.log"
        max_size: "50M"
        max_age: "3d"
        compress: false
    ```

4.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i inventory.ini syslog_rotator.yml
    ```

### Testing

Automated tests are included to verify the playbook's behavior. These tests use `molecule` and mock the system's log file state.

To run tests:
```bash
cd ansible-playbooks/nightly-ansible-syslog-rotator
molecule test
```

### License

This utility is licensed under the MIT License.
