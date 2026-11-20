# Nightly Config Constellation Mapper

## Summary

The `nightly-config-constellation-mapper` is an Ansible playbook designed to help you visualize configuration consistency across your server fleet. It fetches specified configuration files from your target hosts, calculates their SHA256 hashes, and then generates a "constellation map" report. This report groups hosts that have identical configurations for the monitored files, making it easy to spot configuration drift or ensure uniformity.

Think of it as charting the stars of your infrastructure: each star represents a unique configuration state, and servers clustered under the same star are perfectly aligned.

## Features

*   **Configuration Drift Detection**: Quickly identify servers whose configurations deviate from a baseline or from their peers.
*   **Consistency Visualization**: Get a clear, human-readable report showing which servers share identical configurations.
*   **Customizable Monitoring**: Easily define which configuration files to monitor.
*   **Ansible Native**: Leverages standard Ansible modules for secure and efficient operation.

## Usage

1.  **Define your Inventory**: Create an `inventory.ini` file listing your target hosts.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    db2.example.com
    ```

2.  **Specify Configuration Files**: Edit `src/vars/main.yml` to list the paths of the configuration files you want to monitor.

    ```yaml
    # src/vars/main.yml
    config_files_to_monitor:
      - /etc/nginx/nginx.conf
      - /etc/fstab
      - /etc/ssh/sshd_config
    ```

3.  **Run the Playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/constellation_mapper.yml
    ```

    The playbook will output the constellation report to standard output.

## Example Output

```
--- CONFIGURATION CONSTELLATION MAP ---

Constellation 1 (Hash: a1b2c3d4e5f6...)
  - web1.example.com
  - web2.example.com

Constellation 2 (Hash: f7e8d9c0b1a2...)
  - db1.example.com

Constellation 3 (Hash: 1a2b3c4d5e6f...)
  - db2.example.com

---------------------------------------
```

## Requirements

*   Ansible (version 2.9 or newer recommended)
*   Python 3 on the control node and target hosts.
*   SSH access to target hosts with appropriate permissions to read specified configuration files.

## Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_constellation_mapper.yml --connection=local
```

The tests use `ansible.builtin.set_fact` to mock file content and hashes, then assert the correct grouping of hosts into constellations.
