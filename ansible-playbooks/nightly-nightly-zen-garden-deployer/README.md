# Nightly Zen Garden Deployer

This Ansible playbook deploys and maintains a whimsical "Digital Zen Garden" static website on a target server. It sets up a web server (Nginx), creates a simple HTML page with a placeholder for a zen quote, and schedules a cron job to periodically update this quote from a predefined list.

## Features

-   **Nginx Setup**: Installs and configures Nginx to serve the static site.
-   **Static Site Deployment**: Creates a `/var/www/zen_garden` directory and deploys a basic `index.html`.
-   **Dynamic Zen Quotes**: A cron job periodically updates the `index.html` with a new, randomly selected zen quote.
-   **Self-Contained**: All necessary files and configurations are managed by the playbook.

## Prerequisites

-   Ansible installed on your control machine.
-   SSH access to the target server(s) with `sudo` privileges.
-   Python (for Ansible's remote modules) and Nginx (will be installed by the playbook) on the target server(s).

## Usage

1.  **Define your inventory**:
    Create an `inventory.ini` file (or use an existing one) and add your target server(s) under a group, e.g., `[webservers]`.

    ```ini
    [webservers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    ```

2.  **Customize variables (Optional)**:
    Edit `src/vars/main.yml` to change the `zen_garden_path`, `nginx_conf_path`, or the list of `zen_quotes`.

3.  **Run the playbook**:
    ```bash
    ansible-playbook -i inventory.ini src/deploy_zen_garden.yml --ask-become-pass
    ```
    (The `--ask-become-pass` flag will prompt for your sudo password on the remote host.)

## Example `inventory.ini`

```ini
[zen_servers]
zen_master_1 ansible_host=192.168.1.100 ansible_user=ubuntu
zen_master_2 ansible_host=zen.example.com ansible_user=root
```

## Testing

To run the included tests, ensure you have Ansible installed. The tests use `ansible-playbook` in `check_mode` to verify that tasks would correctly register changes without actually modifying your local system.

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_deploy_zen_garden.yml
```
