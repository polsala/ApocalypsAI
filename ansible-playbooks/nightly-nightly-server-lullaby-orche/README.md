# Nightly Server Lullaby Orchestrator

This Ansible playbook helps you gently "tuck in" your non-production or development servers for the night. It performs a series of actions to ensure they are in a calm, optimized state, ready for a good night's rest, and leaves a whimsical goodnight message.

## Features

- **Service Management**: Stops a configurable list of non-essential services.
- **Temporary File Cleanup**: Clears specified temporary directories.
- **Log Rotation/Truncation**: Ensures logs are managed (example provided).
- **Whimsical Goodnight Message**: Leaves a custom message on the server.

## Usage

1.  **Inventory**: Prepare your `src/inventory.ini` file with the servers you want to tuck in.
    ```ini
    [servers]
    your_server_1 ansible_host=192.168.1.10
    your_server_2 ansible_host=192.168.1.11
    ```

2.  **Configuration**: Customize `vars/lullaby_config.yml` to define which services to stop, which paths to clean, and your desired goodnight message.

    ```yaml
    # vars/lullaby_config.yml
    lullaby_services_to_stop:
      - apache2
      - nginx
    lullaby_temp_paths_to_clean:
      - /tmp/*
      - /var/tmp/*
    lullaby_goodnight_message_path: /etc/motd.d/lullaby_message
    lullaby_goodnight_message_content: |
      "Shhh... the servers are sleeping now.
      Dream of efficient processes and minimal resource usage.
      See you in the morning, bright and refreshed!"
    ```

3.  **Run the Playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/lullaby.yml
    ```

    For a dry run (check mode):
    ```bash
    ansible-playbook -i src/inventory.ini src/lullaby.yml --check
    ```

## Automated Tests

The tests use a local connection and `assert` tasks to verify the playbook's logic without actual service manipulation or file deletion on a remote system. It creates mock files and service indicators, runs the playbook, and then asserts the expected state changes.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_lullaby.yml
```

The `tests/inventory_test.ini` uses `ansible_connection=local` and `ansible_python_interpreter=/usr/bin/python3` to run tasks directly on the localhost for testing purposes.
