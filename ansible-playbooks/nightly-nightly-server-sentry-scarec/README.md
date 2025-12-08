# Nightly Server Sentry Scarecrow

This Ansible playbook acts as a whimsical "digital scarecrow" for your servers. It periodically scans for idle processes, high resource consumers, and general digital clutter, then generates a report to help you maintain a clean and efficient server environment. Think of it as a friendly ghost that tidies up your digital garden!

## Features

- Identifies processes consuming high CPU or memory.
- Detects long-running idle processes.
- Audits disk space usage.
- Generates a comprehensive report of findings and suggested "scarecrow actions."

## Prerequisites

- Ansible installed on your control machine.
- SSH access to your target servers (passwordless SSH recommended).
- Python 3 on target servers (Ansible's default connection method requires it).

## Usage

1.  **Define your inventory:**
    Create or update an `inventory.ini` file with your target servers.

    ```ini
    [servers]
    server1.example.com
    server2.example.com
    ```

2.  **Configure scarecrow rules (optional):**
    Review and modify `vars/scarecrow_rules.yml` to adjust thresholds for CPU, memory, idle process age, and processes to ignore.

3.  **Run the playbook:**
    Execute the playbook from your control machine.

    ```bash
    ansible-playbook -i inventory.ini scarecrow_playbook.yml
    ```

    The playbook will generate a `scarecrow_report_{{ ansible_hostname }}.txt` file on each target server (or locally if `report_local_path` is set in `scarecrow_rules.yml`) detailing its findings.

## Configuration (`vars/scarecrow_rules.yml`)

```yaml
# Thresholds for identifying resource-hungry processes
high_cpu_threshold: 80  # Percentage CPU
high_mem_threshold: 70  # Percentage Memory

# Threshold for identifying high disk usage
high_disk_threshold: 85 # Percentage disk usage

# Threshold for identifying long-running idle processes
idle_process_age_hours: 24 # Processes running longer than this without activity (approximation)

# List of processes to ignore during monitoring (e.g., essential system services)
ignored_processes:
  - sshd
  - systemd
  - rsyslogd
  - cron
  - kworker

# Path to save the report on the target host.
report_path: "/tmp/scarecrow_report_{{ ansible_hostname }}.txt"
```

## Testing

To run the automated tests, which use `set_fact` to mock remote system outputs:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_scarecrow_playbook.yml
```

This will run the playbook against `localhost` with predefined mock data and assert that the generated report contains expected warnings.
