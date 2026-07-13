# Nightly Digital Dust Bunny Sweeper

This Ansible playbook, affectionately known as the "Digital Dust Bunny Sweeper," is designed to maintain the pristine condition of your digital infrastructure. It diligently sweeps away accumulated digital detritus, verifies the health of critical services, and reports on disk space, ensuring your systems remain nimble and resilient in the face of the apocalypse (or just Tuesday).

## Features

*   **Digital Dust Bunny Removal**: Cleans temporary files, old logs, and other digital clutter.
*   **Critical Service Vigilance**: Checks the status of essential system services.
*   **Disk Space Scrutiny**: Monitors disk usage to prevent storage bottlenecks.
*   **Cleanliness Report**: Generates a whimsical yet informative report on the system's state.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target hosts with appropriate permissions (e.g., `sudo` access for cleanup tasks).

2.  **Inventory Setup**:
    Create an `inventory.ini` file (or use the provided `src/inventory.ini` as a template) listing your target hosts. Example:

    ```ini
    [servers]
    server1.example.com
    server2.example.com

    [all:vars]
    ansible_user=your_ssh_user
    ansible_become=yes
    ```

3.  **Run the Sweeper**:
    Execute the playbook from your control machine:

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_sweeper.yml
    ```

    To specify a custom report path (default is `/tmp/digital_cleanliness_report.txt` on the target host):

    ```bash
    ansible-playbook -i src/inventory.ini src/dust_sweeper.yml -e "report_path=/var/log/cleanliness_report.txt"
    ```

4.  **Review the Report**:
    After the playbook runs, a `digital_cleanliness_report.txt` (or your specified path) will be generated on each target host. Review this file for insights into your system's cleanliness and health.

## Configuration

You can customize the playbook's behavior by passing variables via `-e` or defining them in `vars/main.yml` (not included by default, but can be added):

*   `report_path`: Path where the cleanliness report will be saved on the target host (default: `/tmp/digital_cleanliness_report.txt`).
*   `log_cleanup_paths`: A list of paths to old log files/directories to clean (default: `["/var/log/*.gz", "/var/log/*.old"]`).
*   `tmp_cleanup_paths`: A list of paths to temporary directories to clean (default: `["/tmp/*", "/var/tmp/*"]`).
*   `critical_services`: A list of service names to check (default: `["sshd", "nginx"]`).
*   `disk_check_paths`: A list of mount points to check disk usage for (default: `["/", "/var"]`).

## Testing

To run the included tests, ensure you have Ansible installed and execute:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_sweeper.yml --connection=local
```

This will simulate a system state, run the sweeper, and assert that cleanup and reporting occur as expected without affecting your actual production systems.
