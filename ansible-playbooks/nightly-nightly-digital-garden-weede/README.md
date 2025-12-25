# Nightly Digital Garden Weeder

## Summary
This Ansible playbook acts as a 'Digital Garden Weeder', helping to keep your servers tidy by pruning unused packages and identifying (and optionally removing) old configuration files. It helps reclaim disk space and reduces configuration clutter, promoting a healthier server environment.

## Features
-   **Package Pruning**: Automatically removes unused packages and dependencies using the system's package manager (apt for Debian/Ubuntu, yum for RedHat/CentOS).
-   **Old Configuration File Detection**: Scans specified directories for configuration files that match certain patterns (e.g., `.bak`, `.old`, `~`) and are older than a defined threshold.
-   **Weeding Report**: Generates a detailed report summarizing the packages pruned and the old configuration files found.
-   **Optional Removal**: Provides an option to remove the identified old configuration files, ensuring safety by requiring an explicit tag.

## Usage

### Prerequisites
-   Ansible installed on your control machine.
-   SSH access to your target servers with appropriate permissions (e.g., sudo).

### 1. Configure Inventory
Edit the `inventory.ini` file to list your target servers. For local execution, `localhost` is pre-configured.

```ini
[garden_servers]
localhost ansible_connection=local
# Add your remote servers here:
# server1.example.com
# server2.example.com
```

### 2. Customize Variables (Optional)
Review and modify `vars/main.yml` to adjust the paths to scan, patterns for old files, and the age threshold for configuration files.

```yaml
---
garden_weeder_config_paths:
  - /etc
  - /var/log
  - /opt
garden_weeder_old_config_patterns:
  - "*.bak"
  - "*.old"
  - "*~"
  - "*.tmp"
garden_weeder_config_age_threshold: "30d" # Files older than 30 days
```

### 3. Run the Weeder
Execute the `run_weeder.sh` script to start the digital weeding process. This will prune packages and generate a report of old configuration files.

```bash
./run_weeder.sh
```

### 4. Review the Report
After execution, a report named `weeding_report_<hostname>.txt` will be generated in the playbook directory for each target host. Review this report to see what was pruned and what old configuration files were found.

### 5. Remove Old Configuration Files (Optional)
If you are satisfied with the list of old configuration files in the report and wish to remove them, run the playbook again with the `--tags remove_old_configs` option:

```bash
./run_weeder.sh --tags remove_old_configs
```

**WARNING**: Always review the report carefully before running with `--tags remove_old_configs` to avoid unintended data loss.

## Testing
To run the automated tests for this utility, execute the following command:

```bash
ansible-playbook -i inventory.ini tests/test_prune_garden.yml
```

This test playbook uses mocked data to simulate package pruning and old file detection, ensuring the report generation logic works correctly without modifying your system.
