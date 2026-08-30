# Nightly Digital Gnome Keeper

An Ansible playbook to deploy and maintain a whimsical digital garden gnome on your servers. This utility ensures a friendly ASCII art gnome resides in a designated "digital garden" directory and can optionally greet you daily via a cron job.

## Features

*   **Gnome Deployment**: Places a charming ASCII art gnome file on your target systems.
*   **Habitat Management**: Creates and manages the `/opt/digital_garden/gnome` directory with appropriate permissions.
*   **Daily Greetings (Optional)**: Configures a cron job to log a daily greeting from your gnome.
*   **Idempotent**: Running the playbook multiple times will result in the same desired state without unintended side effects.

## Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers (or `connection: local` for local deployment).
*   Python 3 on target servers (for Ansible's `raw` module if needed, though not strictly for this playbook).

## Usage

1.  **Create an Inventory File**:
    Create an `inventory.ini` file specifying your target hosts.

    ```ini
    [garden_servers]
    your_server_ip_or_hostname ansible_user=your_ssh_user ansible_become=yes
    # Add more servers as needed
    ```

    For local testing, you can use:
    ```ini
    [garden_servers]
    localhost ansible_connection=local ansible_become=yes
    ```

2.  **Run the Playbook**:
    Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/gnome_keeper.yml
    ```

    To disable the cron job, you can pass a variable:
    ```bash
    ansible-playbook -i src/inventory.ini src/gnome_keeper.yml -e "enable_gnome_cron=false"
    ```

## Configuration

The playbook uses the following variables, which can be overridden via `--extra-vars` (`-e`) or in your inventory:

*   `gnome_base_dir`: The base directory for the digital garden. Default: `/opt/digital_garden`
*   `gnome_name`: The filename for the gnome. Default: `gnome_buddy.txt`
*   `gnome_owner`: The owner of the gnome files. Default: `root`
*   `gnome_group`: The group of the gnome files. Default: `root`
*   `gnome_dir_mode`: Permissions for the gnome directory. Default: `0755`
*   `gnome_file_mode`: Permissions for the gnome file. Default: `0644`
*   `enable_gnome_cron`: Whether to enable the daily cron greeting. Default: `true`
*   `gnome_cron_log_file`: Path to the log file for gnome greetings. Default: `/var/log/gnome_greetings.log`

## Example Output (after running playbook)

```
# On your server, check the directory:
ls -l /opt/digital_garden/gnome/
# Expected: -rw-r--r-- 1 root root <size> <date> gnome_buddy.txt

# View the gnome:
cat /opt/digital_garden/gnome/gnome_buddy.txt

# If cron is enabled, check cron jobs:
sudo crontab -l | grep "gnome_buddy.txt"
# Expected: 0 8 * * * cat /opt/digital_garden/gnome/gnome_buddy.txt >> /var/log/gnome_greetings.log 2>&1

# Check the log file after a day:
cat /var/log/gnome_greetings.log
# Expected: (gnome art)
```

## Testing

The `tests/run_tests.sh` script orchestrates the testing process. It first cleans up any previous deployments, then runs the main `gnome_keeper.yml` playbook, verifies the deployed state using `tests/verify.yml`, and finally cleans up again.

To run the tests:

```bash
bash tests/run_tests.sh
```

This will execute the playbook against `localhost` using `ansible_connection=local`, ensuring deterministic and offline testing without requiring remote infrastructure.
