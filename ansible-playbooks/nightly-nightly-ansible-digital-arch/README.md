# Nightly Ansible Digital Archivist

This Ansible playbook, `nightly-ansible-digital-archivist`, helps you maintain a consistent and timestamped archive of important digital artifacts (files, notes, logs) across your remote servers. It ensures that specified files are copied to a designated archive directory, with a timestamp appended to their names, providing a historical record of your digital assets.

## Features

*   **Automated Archiving**: Automatically identifies and archives files from configurable source paths.
*   **Timestamping**: Appends a configurable timestamp (e.g., `_YYYYMMDDHHMMSS`) to archived file names for easy versioning and historical tracking.
*   **Configurable Paths**: Easily define source directories and the target archive location.
*   **Idempotent**: Designed to be run multiple times without unintended side effects (though new archives will be created if source files change or on subsequent runs).

## Prerequisites

*   **Ansible**: Installed on your control machine.
*   **SSH Access**: To your target hosts from the control machine.
*   **Python**: On target hosts (required for some Ansible modules).
*   **`community.general` collection**: Install with `ansible-galaxy collection install community.general` if not already present.

## Usage

1.  **Define your Inventory**:
    Create an `inventory.ini` file (or use an existing one) listing your target hosts.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```

2.  **Configure Variables**:
    Edit `src/vars/main.yml` to specify the `archive_base_dir` on the remote hosts and the `source_paths` to monitor.

    ```yaml
    # src/vars/main.yml
    archive_base_dir: "/var/local/digital_archive"
    source_paths:
      - "/var/log/myapp"
      - "/etc/configs"
      - "/home/user/notes"
    timestamp_format: "_%Y%m%d%H%M%S" # Format for the timestamp suffix
    ```

3.  **Run the Playbook**:
    Execute the playbook from your control machine:

    ```bash
    ansible-playbook -i inventory.ini src/archive_artifacts.yml
    ```

    To perform a dry run without making any changes:

    ```bash
    ansible-playbook -i inventory.ini src/archive_artifacts.yml --check
    ```

## Playbook Structure

*   `src/archive_artifacts.yml`: The main Ansible playbook.
*   `src/inventory.ini`: Example inventory file.
*   `src/vars/main.yml`: Variables for configuring archive paths and sources.
*   `tests/test_archive_artifacts.yml`: A test playbook to verify functionality.

## How it Works

The playbook performs the following steps on each target host:

1.  Ensures the `archive_base_dir` exists.
2.  Uses the `community.general.find` module to locate files within the `source_paths`.
3.  For each found file, it constructs a new filename by appending the current timestamp based on `timestamp_format`.
4.  Copies the file to the `archive_base_dir` using the new timestamped name.

## Testing

To run the tests, ensure Ansible is installed. The tests simulate remote operations on `localhost` by creating temporary files and directories.

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_archive_artifacts.yml
```

The test playbook will:
1.  Create temporary source directories and files on `localhost`.
2.  Run the main `archive_artifacts.yml` playbook, targeting `localhost`.
3.  Verify that the timestamped archived files exist in the expected location.
4.  Clean up the temporary directories and files.
