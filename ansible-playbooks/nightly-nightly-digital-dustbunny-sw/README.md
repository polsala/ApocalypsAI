## Nightly Digital Dustbunny Sweeper

### Summary
This Ansible playbook is designed to help maintain a pristine digital environment by sweeping away "digital dustbunnies" – old, temporary files, forgotten caches, and stale log entries that accumulate over time. It identifies files older than a specified age in designated directories and removes them, then generates a whimsical report of the cleanup operation.

### Usage

1.  **Define your inventory**: Create an `inventory.ini` file (or use the provided `src/inventory.ini`) listing the servers you wish to clean. Ensure Ansible can connect to these servers (e.g., via SSH keys).

    ```ini
    [servers]
    your_server_1.example.com
    your_server_2.example.com
    # ... add more servers
    ```

2.  **Configure cleanup parameters**: Edit `src/vars/main.yml` to specify the paths to scan and the age threshold for files to be considered dustbunnies.

    ```yaml
    cleanup_paths:
      - /tmp
      - /var/log/old_app_data
      - /var/cache/apt/archives
    cleanup_age_days: 30 # Files older than 30 days will be swept
    report_output_path: /tmp/dustbunny_cleanup_report.txt # Path to save the report on the Ansible controller
    ```

3.  **Run the playbook**: Execute the main playbook using Ansible.

    ```bash
    ansible-playbook -i src/inventory.ini src/dustbunny_sweeper.yml
    ```

    The playbook will connect to your specified servers, find and delete old files, and generate a cleanup report on the Ansible controller.

### Configuration

-   `src/inventory.ini`: Standard Ansible inventory file. Modify to target your specific hosts.
-   `src/vars/main.yml`: Contains configurable variables:
    -   `cleanup_paths`: A list of absolute paths where the sweeper will look for old files.
    -   `cleanup_age_days`: An integer representing the number of days. Files older than this will be removed.
    -   `report_output_path`: The path on the Ansible controller where the whimsical cleanup report will be saved.

### Testing

To ensure the Digital Dustbunny Sweeper is working as intended without affecting your production systems, you can run the provided test playbook. This test creates a temporary directory, populates it with files of varying ages, runs the core sweeping logic against it, and then asserts that only the old files were removed.

1.  **Ensure Ansible is installed** on your local machine.

2.  **Run the test playbook**:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_dustbunny_sweeper.yml
    ```

    The test will output success or failure messages based on its assertions. Upon completion, the temporary test directory and its contents will be cleaned up.
