# Nightly Survival Kit Provisioner

This Ansible playbook, `nightly-survival-kit-provisioner`, is designed to quickly provision a server with essential tools and baseline security configurations, preparing it for any eventuality – from a digital wasteland to a full-blown apocalypse.

It ensures your server has critical utilities, a basic firewall, and a system health check script, making it a resilient outpost in uncertain times.

## Features

*   **Essential Tools**: Installs a curated list of indispensable packages (e.g., `htop`, `tmux`, `git`, `vim`, `curl`, `jq`).
*   **Firewall Configuration**: Sets up and enables UFW (Uncomplicated Firewall) with basic rules for SSH, HTTP, and HTTPS.
*   **System Health Check**: Deploys a simple bash script to monitor disk, memory, and CPU usage.
*   **Time Synchronization**: Ensures NTP is installed and running for accurate timekeeping.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target server(s) with `sudo` privileges.

2.  **Inventory**: Update the `src/inventory.ini` file with your target server(s) information. For local execution, `localhost` is pre-configured.

    ```ini
    [survival_servers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    
    [all:vars]
    ansible_python_interpreter=/usr/bin/python3
    ```

3.  **Run the Playbook**: Execute the playbook using the `ansible-playbook` command.

    ```bash
    ansible-playbook -i src/inventory.ini src/survival_kit.yml --ask-become-pass
    ```
    (The `--ask-become-pass` flag will prompt for your `sudo` password on the target machine if needed.)

4.  **Verify**: After execution, you can log into your server and check for installed packages (`htop`), UFW status (`sudo ufw status`), and the health script (`sudo /usr/local/bin/survival_health_check.sh`).

## Configuration

*   **`vars/main.yml`**: Contains the list of `survival_packages` to be installed. You can customize this list to include or remove tools as per your survival strategy.

## Testing

To ensure the playbook functions as expected without making actual changes to your system, you can run the provided test playbook in `check_mode`.

```bash
ansible-playbook -i src/inventory.ini tests/test_survival_kit.yml
```

This test playbook will execute each task from `src/survival_kit.yml` in `check_mode` (dry run) and assert that they *would* report changes on a fresh system. This verifies the playbook's logic and idempotency without modifying your environment.
