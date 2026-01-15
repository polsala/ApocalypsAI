# Nightly Digital Dust Bunny Sweeper

This Ansible playbook helps maintain digital hygiene across your servers by identifying "digital dust bunnies" – old, unused files, packages, and inactive services that might be cluttering your systems or posing potential security risks. It generates a comprehensive report without making any changes to your systems, allowing you to review and decide on cleanup actions.

## Features

*   **File Age Scan**: Identifies files older than a configurable threshold in specified directories.
*   **Unused Package Scan**: Lists installed packages that haven't been accessed or updated recently (requires some heuristics, or just lists all packages for review).
*   **Inactive Service Scan**: Reports on services that are installed but not currently running.
*   **Comprehensive Reporting**: Generates a human-readable report summarizing all findings.
*   **Non-Destructive**: Only reports findings; no files are deleted, packages uninstalled, or services stopped.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers.

### 1. Inventory

Create an `inventory.ini` file listing your target servers.

```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
```

### 2. Configuration (Optional)

You can customize the "dust" detection rules by modifying `vars/dust_rules.yml` or passing extra variables.

```yaml
# vars/dust_rules.yml
---
file_age_threshold_days: 365 # Files older than this will be flagged
scan_directories:
  - /tmp
  - /var/log
  - /opt
  - /usr/local/bin
package_ignore_patterns:
  - "^kernel-" # Example: ignore kernel packages
service_ignore_patterns:
  - "ssh" # Example: ignore ssh service
```

### 3. Run the Playbook

Execute the playbook from your control machine:

```bash
ansible-playbook -i inventory.ini dust_sweeper.yml
```

The playbook will connect to your servers, gather information, and generate a report. The report will be saved to a file named `dust_report_{{ ansible_hostname }}.txt` in the directory where you run the playbook.

### 4. Review the Report

Examine the generated `dust_report_*.txt` files for each host to identify potential cleanup candidates.

## How it Works

The playbook uses various Ansible modules (`find`, `package_facts`, `service_facts`, `command`) to gather data from remote hosts. It then processes this data to filter for items matching the "dust" criteria and compiles them into a structured report using a Jinja2 template.

## Testing

To run the included tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_dust_sweeper.yml
```

This will run the playbook against a local mock environment and verify the report generation logic.
