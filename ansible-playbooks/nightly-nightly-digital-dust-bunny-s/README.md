# Nightly Digital Dust Bunny Sweeper

## Summary
This Ansible playbook helps maintain system hygiene by identifying and optionally cleaning up old, unused, or temporary files (affectionately termed "digital dust bunnies") on your remote servers. It generates a report detailing the files found and can be configured for a dry run or actual deletion.

## How it Works
1.  **Configuration**: Define `scan_paths`, `file_age_days`, and `dry_run` in `vars/main.yml`.
2.  **Discovery**: The playbook uses Ansible's `find` module to locate files older than the specified `file_age_days` within the `scan_paths`.
3.  **Reporting**: A detailed report is generated (using a Jinja2 template) listing all identified "dust bunnies". This report is saved to `report_path` on the Ansible control machine.
4.  **Action (Optional)**: If `dry_run` is set to `false`, the playbook proceeds to delete the identified files. Otherwise, it only reports them.

## Prerequisites
*   Ansible installed on your control machine.
*   SSH access to your target servers from the control machine.
*   Python 3 on target servers (for Ansible modules).

## Usage

1.  **Clone the repository** (if you haven't already).
2.  **Navigate** to the `ansible-playbooks/nightly-digital-dust-bunny-sweeper` directory.
3.  **Configure your inventory**: Edit `inventory.ini` to list your target servers.
    ```ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```
4.  **Configure variables**: Edit `vars/main.yml` to define your scan paths, age threshold, and whether to perform a dry run.
    ```yaml
    ---
    scan_paths:
      - "/tmp/digital_dust_bunnies" # Paths to scan for old files
      - "/var/log/old_app_logs"
    file_age_days: 30 # Files older than 30 days will be considered dust bunnies
    dry_run: true # Set to false to actually delete files
    report_path: "/tmp/dust_bunny_sweeper_report_{{ ansible_hostname }}.txt" # Report path on control machine
    ```
5.  **Run the playbook (Dry Run first!)**:
    It's highly recommended to run in `dry_run: true` mode first to review the report before deleting any files.
    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml
    ```
    After execution, check the report file (e.g., `/tmp/dust_bunny_sweeper_report_localhost.txt` if running against localhost) for details.

6.  **Run for actual cleanup (if satisfied with dry run report)**:
    Change `dry_run: false` in `vars/main.yml` and run again.
    ```bash
    ansible-playbook -i inventory.ini dust_bunny_sweeper.yml
    ```

## Testing

To run the automated tests for this utility:

1.  Ensure Ansible is installed.
2.  Navigate to the `ansible-playbooks/nightly-digital-dust-bunny-sweeper/tests` directory.
3.  Execute the test runner script:
    ```bash
    ./test_runner.sh
    ```
    This script will set up mock files, run the main playbook in dry-run and cleanup modes, and verify the outcomes.
