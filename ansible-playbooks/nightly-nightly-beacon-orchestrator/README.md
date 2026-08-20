# Nightly Survival Beacon Orchestrator

## Summary

In the post-apocalyptic landscape, reliable communication is paramount. The `nightly-beacon-orchestrator` is an Ansible playbook designed to deploy and maintain a network of 'survival beacon' services. These beacons are simple web servers broadcasting a status page, ensuring that critical communication points are operational and visible across your distributed infrastructure.

This utility ensures that a basic web server (Nginx by default) is installed, a custom 'beacon status' page is deployed, and the service is running on designated 'beacon' hosts. It's a whimsical yet practical way to monitor the basic health and reachability of your critical nodes.

## Features

*   **Nginx Installation**: Ensures Nginx is installed and configured.
*   **Beacon Status Page**: Deploys a dynamic HTML page indicating the beacon's operational status and host details.
*   **Service Management**: Guarantees the Nginx service is running and restarts it upon configuration changes.
*   **Idempotent**: Can be run repeatedly without unintended side effects.

## Prerequisites

*   **Ansible**: Installed on your control machine.
*   **SSH Access**: Passwordless SSH access (or SSH agent forwarding) to your target 'beacon' hosts.
*   **Sudo Privileges**: The Ansible user on target hosts must have `sudo` privileges to install packages and manage services.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file (or modify the provided `src/inventory.ini`) listing your beacon hosts under the `[beacons]` group.

    ```ini
    [beacons]
    beacon1.example.com
    beacon2.example.com
    192.168.1.10
    ```

2.  **Run the playbook**: Execute the main playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml
    ```

    To perform a dry run without making any changes:

    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml --check
    ```

3.  **Verify**: After successful execution, navigate to `http://<beacon_host_ip_or_hostname>/beacon_status.html` in your web browser to see the operational status page.

## Directory Structure

```
. 
├── README.md
├── src/
│   ├── inventory.ini
│   ├── playbook.yml
│   └── roles/
│       └── beacon_service/
│           ├── handlers/
│           │   └── main.yml
│           ├── tasks/
│           │   └── main.yml
│           └── templates/
│               └── beacon_status.html.j2
└── tests/
    └── test_playbook.yml
```

## Customization

*   **Web Server**: The role currently uses Nginx. To change to Apache or another web server, modify `roles/beacon_service/tasks/main.yml` accordingly.
*   **Status Page Content**: Edit `roles/beacon_service/templates/beacon_status.html.j2` to customize the beacon's status message or add more dynamic information.
*   **Port**: By default, Nginx listens on port 80. If you need a different port, modify the Nginx configuration within the role.

## Contributing

Feel free to enhance the beacon's capabilities, add more robust monitoring, or integrate with other post-apocalyptic communication systems!
