# Nightly Wasteland Data Fortifier

An Ansible playbook designed to fortify critical "Wasteland Data Archive" services. In a post-apocalyptic world, data integrity and availability are paramount. This utility ensures that your vital data archives are running, their storage locations are properly secured, and regular backup mechanisms are in place.

## Features

*   **Service Assurance**: Ensures the specified data archive service is running.
*   **Directory Fortification**: Verifies and sets appropriate permissions for the data storage directory.
*   **Backup Automation**: Deploys a simple backup script and schedules it via cron.
*   **Idempotent**: Can be run multiple times without causing unintended side effects.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to the target machines where the data archive service runs.
*   Python installed on the target machines (required for Ansible modules).

### Inventory

Create an `inventory.ini` file specifying your target hosts.

```ini
[wasteland_archives]
archive_server_1 ansible_host=192.168.1.10
archive_server_2 ansible_host=192.168.1.11
```

### Variables

You can customize the following variables in `src/vars/main.yml` or by passing them via `--extra-vars`:

*   `data_archive_service_name`: The name of the data archive service (e.g., `wasteland-archive`).
*   `data_archive_path`: The absolute path to the data storage directory (e.g., `/opt/wasteland_data`).
*   `backup_script_path`: The path where the backup script will be deployed (e.g., `/usr/local/bin/backup_wasteland_data.sh`).
*   `backup_cron_schedule`: The cron schedule for the backup script (e.g., `"0 2 * * *"`, for 2 AM daily).
*   `backup_destination_path`: The directory where backups will be stored (e.g., `/mnt/backup_drive`).

### Running the Playbook

To fortify your wasteland data archives:

```bash
ansible-playbook -i src/inventory.ini src/fortify_data_archive.yml
```

To run with custom variables:

```bash
ansible-playbook -i src/inventory.ini src/fortify_data_archive.yml \
  --extra-vars "data_archive_service_name=my_custom_archive data_archive_path=/var/lib/my_archive"
```

## Testing

This utility includes a self-contained test playbook that can be run locally.

### Prerequisites for Testing

*   Ansible installed.

### Running Tests

```bash
ansible-playbook -i src/inventory.ini tests/test_fortify_data_archive.yml
```

The test playbook will:
1.  Set up a temporary environment on `localhost`.
2.  Run the main `fortify_data_archive.yml` playbook against this temporary environment.
3.  Verify that all expected files, directories, permissions, and cron jobs are correctly configured.
4.  Run the main playbook again in `check_mode` to ensure idempotence (no changes reported on a fortified system).
5.  Clean up the temporary environment.
