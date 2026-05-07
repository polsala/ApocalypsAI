# Nightly Service Sentinel

The Nightly Service Sentinel is an Ansible playbook designed to vigilantly monitor critical systemd services across your infrastructure. In the face of digital entropy, this sentinel ensures your essential services remain operational. Should a service be found in a "deceased" state, the sentinel will attempt a swift "resurrection" and log the event with appropriate gravitas.

## Features

*   **Vigilant Monitoring**: Checks the status of specified systemd services.
*   **Automatic Resurrection**: Attempts to start services found to be inactive or failed.
*   **Whimsical Logging**: Provides dramatic output for service status changes.
*   **Configurable**: Easily define which services to monitor via variables.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file listing the hosts where you want to run the sentinel.

    ```ini
    [servers]
    server1.example.com
    server2.example.com

    [all:vars]
    ansible_user=your_ssh_user
    ansible_become=true
    ```

2.  **Configure services**: Edit `vars/main.yml` to specify the services you wish to monitor.

    ```yaml
    # vars/main.yml
    ---
    critical_services:
      - nginx
      - postgresql
      - my_custom_app
    ```

    Alternatively, pass them as extra-vars when running the playbook:
    `ansible-playbook -i inventory.ini src/service_sentinel.yml -e "critical_services=['nginx', 'redis']"`

3.  **Run the playbook**: 

    ```bash
    ansible-playbook -i inventory.ini src/service_sentinel.yml
    ```

    The playbook will connect to your hosts, check the status of each `critical_service`, and attempt to start any that are not running.

## Testing

This utility includes a self-contained test playbook that simulates service states on `localhost` to ensure the sentinel's logic functions correctly.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_service_sentinel.yml
```

The test playbook will:
1.  Create a dummy systemd service.
2.  Stop the dummy service.
3.  Run the main `service_sentinel.yml` playbook, expecting it to start the dummy service.
4.  Verify the dummy service is running.
5.  Run the main `service_sentinel.yml` playbook again, expecting it to find the service already running.
6.  Clean up the dummy service.

## Requirements

*   Ansible (version 2.9 or higher recommended)
*   Target hosts must be running `systemd`.
*   SSH access to target hosts with `sudo` privileges for the `ansible_user`.
