# Nightly Digital Janitor

## Summary
The `nightly-digital-janitor` is an Ansible playbook designed to keep your servers sparkling clean and free of digital clutter. It automatically tidies up temporary files, archives old logs, removes broken symlinks, and cleans up unused packages, ensuring your systems run smoothly and efficiently. Think of it as a diligent, automated cleaning crew for your digital infrastructure!

## Features
- **Temporary File Cleanup**: Removes old files from `/tmp` and `/var/tmp` directories.
- **Log Archiving**: Moves old log files from `/var/log` to a specified archive directory.
- **Broken Symlink Removal**: Deletes any broken symbolic links found in temporary directories.
- **Package Cleanup**: Runs `apt autoremove` / `apt autoclean` (for Debian-based systems) or `yum autoremove` (for RedHat-based systems) to remove unused packages.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access (or `ansible_connection=local` for localhost) to the target servers with `sudo` privileges.

### Files
- `src/janitor.yml`: The main Ansible playbook.
- `src/inventory.ini`: An example inventory file.
- `src/vars/main.yml`: Default variables for cleanup thresholds and paths.

### Configuration
You can customize the cleanup behavior by modifying `src/vars/main.yml` or by passing `--extra-vars` during playbook execution.

**`src/vars/main.yml`**:
```yaml
# Number of days after which temporary files are considered "old" and will be removed.
tmp_cleanup_days: 7

# Number of days after which log files are considered "old" and will be archived.
log_cleanup_days: 30

# The path where old log files will be moved.
log_archive_path: "/var/log/archive"

# Paths for temporary file cleanup (can be overridden via --extra-vars for testing)
cleanup_tmp_path: "/tmp"
cleanup_var_tmp_path: "/var/tmp"
cleanup_log_path: "/var/log"
```

### Running the Playbook

1.  **Prepare your inventory**:
    Ensure your `src/inventory.ini` (or your custom inventory file) lists the hosts you want to clean. For a quick local test, the provided `inventory.ini` is sufficient.

    ```ini
    [servers]
    your_server_ip_or_hostname
    ```
    Or for localhost:
    ```ini
    [localhost]
    localhost ansible_connection=local
    ```

2.  **Execute the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/janitor.yml --ask-become-pass
    ```
    (Use `--ask-become-pass` if your user requires a password for `sudo`.)

    To run against localhost without a password (if your user has passwordless sudo or is already root):
    ```bash
    ansible-playbook -i src/inventory.ini src/janitor.yml --connection=local --limit=localhost --become
    ```

3.  **Customize on the fly**:
    You can override variables directly from the command line:
    ```bash
    ansible-playbook -i src/inventory.ini src/janitor.yml --extra-vars "tmp_cleanup_days=3 log_cleanup_days=15"
    ```

## Automated Tests

The utility includes a Python-based test suite (`tests/test_janitor.py`) that ensures the playbook's functionality in a deterministic and isolated environment.

### Running Tests
1.  **Install dependencies**:
    ```bash
    pip install PyYAML
    ```
    (Ansible itself is a dependency for running the playbook, but `PyYAML` is needed for the Python test script to parse `extra_vars`.)

2.  **Execute the tests**:
    ```bash
    python -m unittest tests/test_janitor.py
    ```

The tests work by:
- Creating a temporary directory structure with mock old/new files, logs, and broken symlinks.
- Running the `janitor.yml` playbook against `localhost` using `ansible_connection=local`, directing it to clean the temporary directories via `--extra-vars`.
- Asserting that the expected files have been removed or archived, and broken symlinks are gone, without affecting the actual system.
- Performing a syntax check on the playbook YAML.
