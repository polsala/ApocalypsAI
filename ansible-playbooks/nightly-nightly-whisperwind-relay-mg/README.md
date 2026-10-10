# Nightly Whisperwind Relay Manager

An Ansible playbook to deploy and manage a 'Whisperwind Message Relay' service that periodically logs cryptic messages from the void.

## Purpose

In the quiet hum of the post-apocalyptic network, sometimes you just need a little... whisper. This utility deploys a simple Python script to your target systems that acts as a "Whisperwind Relay." Periodically, it fetches a cryptic message (a "whisper") and logs it locally. It's a whimsical way to ensure your systems are not entirely devoid of existential musings, or perhaps, subtle warnings.

## Features

*   **Automated Deployment**: Installs the relay script and its data file.
*   **Cron Integration**: Sets up a cron job to run the relay script at a configurable interval.
*   **Log Management**: Ensures a dedicated log file for whispers.
*   **Idempotent**: Can be run multiple times without side effects.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target machines (if deploying remotely).
*   Python 3 installed on target machines.

### Files

*   `src/deploy_relay.yml`: The main Ansible playbook.
*   `src/inventory.ini`: Example inventory file.
*   `src/whisper_relay.py`: The Python script that fetches and logs whispers.
*   `src/whispers.txt`: A collection of cryptic messages.
*   `tests/test_deploy_relay.yml`: Ansible playbook for testing the deployment.

### Deployment

1.  **Configure Inventory**:
    Edit `src/inventory.ini` to include your target hosts. For local testing, `localhost` is pre-configured.

    ```ini
    [whisper_hosts]
    localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3
    # Add your remote hosts here:
    # your_server_ip_or_hostname ansible_user=your_ssh_user ansible_become_pass=your_sudo_pass
    ```

    *Replace `your_server_ip_or_hostname`, `your_ssh_user`, and `your_sudo_pass` with your actual details if deploying remotely.* If using `ansible_become_pass`, you might need to provide it interactively or via Ansible Vault.

2.  **Run the Playbook**:
    Execute the playbook from the root of this utility's directory:

    ```bash
    ansible-playbook -i src/inventory.ini src/deploy_relay.yml --ask-become-pass
    ```

    (The `--ask-become-pass` flag is needed if `ansible_become_pass` is not set in inventory or vault, or if your SSH user requires a password for `sudo`.)

### Configuration

You can override variables by passing them with `-e` or by creating a `vars/main.yml` file in the `src/` directory.

*   `relay_base_dir`: Base directory for the relay service (default: `/opt/whisperwind_relay`).
*   `whisper_script_path`: Full path to the Python script (derived from `relay_base_dir`).
*   `whispers_data_path`: Full path to the whispers data file (derived from `relay_base_dir`).
*   `whisper_log_file`: Path to the log file (default: `/var/log/whisperwind_relay.log`).
*   `cron_interval_minutes`: How often the script runs (e.g., `15` for every 15 minutes, default: `15`).

Example:
```bash
ansible-playbook -i src/inventory.ini src/deploy_relay.yml -e "cron_interval_minutes=5" --ask-become-pass
```

## Testing

To run the automated tests, ensure you have Ansible installed. The tests use a local connection for simplicity and determinism.

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_deploy_relay.yml
```

The `tests/inventory_test.ini` uses `ansible_connection=local` to run tests directly on the control machine, simulating the deployment without needing actual remote hosts.
