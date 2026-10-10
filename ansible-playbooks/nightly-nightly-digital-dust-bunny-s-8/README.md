# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps maintain server hygiene by identifying and removing old, unused files (our 'digital dust bunnies') from specified directories. It targets files older than a configurable age and/or larger than a configurable size, helping to free up disk space and keep your systems tidy.

## Features

*   **Configurable Paths**: Specify which directories to scan for dust bunnies.
*   **Age-based Cleanup**: Remove files older than a set number of days.
*   **Size-based Cleanup**: Remove files larger than a set size (in MB).
*   **Dry Run Mode**: Preview what would be deleted without making changes.
*   **Detailed Report**: Get a summary of identified and removed files.

## Usage

1.  **Inventory**: Prepare an Ansible inventory file (`inventory.ini`) listing the servers you want to clean.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [dbservers]
    db1.example.com
    ```

2.  **Variables**: Configure the cleanup parameters in `vars/main.yml` or pass them via the command line.

    *   `cleanup_paths`: A list of directories to scan (e.g., `["/tmp", "/var/log"]`).
    *   `age_threshold_days`: Files older than this will be considered for deletion (e.g., `30`).
    *   `size_threshold_mb`: Files larger than this will be considered for deletion (e.g., `100`).

    ```yaml
    # vars/main.yml
    cleanup_paths: 
      - /tmp
      - /var/log
    age_threshold_days: 30
    size_threshold_mb: 50
    ```

3.  **Run the Playbook**:

    To perform a **dry run** (recommended first step):
    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml --check
    ```

    To **execute the cleanup**:
    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml
    ```

    You can override variables from the command line:
    ```bash
    ansible-playbook -i src/inventory.ini src/dust_bunny_sweeper.yml -e "cleanup_paths=['/var/tmp'] age_threshold_days=7"
    ```

## Files

*   `src/dust_bunny_sweeper.yml`: The main Ansible playbook.
*   `src/inventory.ini`: An example inventory file.
*   `vars/main.yml`: Default variables for cleanup configuration.
*   `templates/dust_bunny_report.j2`: Jinja2 template for the cleanup report.
*   `tests/test_dust_bunny_sweeper.yml`: Automated tests for the playbook.

## Testing

The `test_dust_bunny_sweeper.yml` playbook provides a self-contained, offline test suite. It creates a temporary directory, populates it with mock files (some old, some new, some large, some small), runs the main cleanup playbook against this temporary location, and then asserts that only the expected 'dust bunnies' have been removed.

To run the tests:

```bash
ansible-playbook tests/test_dust_bunny_sweeper.yml
```

This will execute the test playbook on your `localhost` and verify the cleanup logic without affecting your actual system files (outside of the temporary test directory).
