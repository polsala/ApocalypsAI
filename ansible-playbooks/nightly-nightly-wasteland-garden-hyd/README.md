# Nightly Wasteland Garden Hydration System

## Summary
This Ansible playbook, `nightly-wasteland-garden-hydrator`, ensures your remote 'wasteland garden plots' (servers) receive their daily 'hydration' by deploying a simple watering script and setting up a cron job to execute it regularly. It's a whimsical way to manage scheduled tasks on your infrastructure.

## How it Works
1.  **Deploy Script**: The playbook copies a `watering_script.sh` to a specified path on your target servers.
2.  **Set Permissions**: It ensures the script is executable.
3.  **Schedule Cron**: It creates a daily cron job that runs the `watering_script.sh` at a configurable time (defaulting to 3 AM).
4.  **Log Hydration**: The `watering_script.sh` itself creates a log file in a designated directory, recording each 'hydration event'.

## Prerequisites
*   **Ansible**: You need Ansible installed on your control machine.
*   **SSH Access**: SSH access to your target 'garden plot' servers, with appropriate permissions (e.g., `sudo` access for cron job management and script deployment).

## Usage
1.  **Define your Garden Plots**: Edit `src/inventory.ini` to list your target servers under the `[garden_plots]` group. For local testing, `localhost` is pre-configured.

    ```ini
    [garden_plots]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

2.  **Run the Playbook**: Execute the playbook from the root of this utility's directory:

    ```bash
    ansible-playbook -i src/inventory.ini src/hydrate_garden.yml
    ```

    If your remote user requires `sudo`:

    ```bash
    ansible-playbook -i src/inventory.ini src/hydrate_garden.yml --ask-become-pass
    ```

## Configuration
You can customize the following variables in `src/hydrate_garden.yml` or by passing them via `--extra-vars`:
*   `garden_script_path`: The destination path for the watering script (default: `/usr/local/bin/wasteland_garden_waterer.sh`).
*   `garden_log_dir`: The directory where hydration logs will be stored (default: `/tmp/wasteland_garden_logs`).
*   `cron_minute`: The minute for the cron job (default: `0`).
*   `cron_hour`: The hour for the cron job (default: `3` for 3 AM).

## Testing
To ensure the playbook works as expected, a dedicated test playbook is provided. It runs against `localhost` and verifies the script deployment, cron job creation, and log file generation.

1.  **Run Tests**: Execute the test playbook:

    ```bash
    ansible-playbook -i src/inventory.ini tests/test_hydrate_garden.yml --ask-become-pass
    ```

    The `--ask-become-pass` is often necessary as the tests involve managing cron jobs and files in system paths, which typically require root privileges.
