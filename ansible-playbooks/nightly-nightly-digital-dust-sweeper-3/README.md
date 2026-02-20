# Nightly Digital Dust Bunny Sweeper

## Summary
This Ansible playbook is your trusty digital broom, designed to keep your servers tidy by sweeping away 'digital dust bunnies' (old, temporary files) and carefully archiving 'ancient data relics' (other forgotten files) from specified paths. It generates a whimsical report of its findings and actions, ensuring your digital realm remains clutter-free and ready for whatever the apocalypse throws your way.

## Features
-   **Digital Dust Bunny Removal**: Identifies and deletes temporary files, old logs, and other ephemeral clutter based on age thresholds.
-   **Ancient Data Relic Archiving**: Moves important-but-old files to a designated 'digital archive' for safekeeping, rather than outright deletion.
-   **Customizable Paths & Ages**: Easily configure which directories to scan and how old files need to be to qualify as dust bunnies or relics.
-   **Comprehensive Report**: Generates a detailed, human-readable report of all files found, deleted, and archived.
-   **Idempotent**: Running the playbook multiple times will achieve the same desired state without unintended side effects.

## Usage

### Prerequisites
-   Ansible installed on your control machine.
-   SSH access to your target servers (if not running locally).

### 1. Configure Inventory
Update `src/inventory.ini` with your target hosts. For local execution, `localhost` is sufficient.

```ini
[servers]
localhost ansible_connection=local
# my_server_1 ansible_host=192.168.1.100 ansible_user=ubuntu
```

### 2. Configure Variables
Edit `src/vars/main.yml` to define your sweep paths, age thresholds, and archive location.

```yaml
# src/vars/main.yml

# Paths to scan for digital dust bunnies (files to be deleted)
# These are typically temporary files, old logs, cache files, etc.
dust_bunny_paths:
  - "/tmp/digital_dust_bunnies"
  - "/var/log/old_logs"

# Files older than this many days will be considered dust bunnies
dust_bunny_age_days: 7

# Paths to scan for ancient data relics (files to be archived)
# These are typically important but inactive data files, old backups, etc.
relic_paths:
  - "/tmp/ancient_relics"
  - "/var/data/old_backups"

# Files older than this many days will be considered relics
relic_age_days: 30

# Directory where ancient data relics will be moved
archive_base_dir: "/var/digital_archive"

# Path for the sweep report
sweep_report_path: "/var/log/digital_dust_sweep_report.txt"
```

### 3. Run the Playbook
Execute the playbook from the `ansible-playbooks/nightly-digital-dust-sweeper` directory:

```bash
ansible-playbook -i src/inventory.ini src/dust_sweeper.yml
```

#### Dry Run (Check Mode)
To see what actions the playbook *would* take without actually making any changes:

```bash
ansible-playbook -i src/inventory.ini src/dust_sweeper.yml --check
```

### 4. Review the Report
After execution, check the generated report at the `sweep_report_path` defined in `src/vars/main.yml` (e.g., `/var/log/digital_dust_sweep_report.txt`).

## Development & Testing

### Running Tests
Tests are located in `tests/test_dust_sweeper.yml`. They use `localhost` and create temporary files to simulate different scenarios. To run them:

```bash
ansible-playbook -i tests/test_inventory.ini tests/test_dust_sweeper.yml
```

### Mock Rationale
The tests create a temporary directory and populate it with files of specific ages to simulate a real server environment. This allows for deterministic testing of the `find`, `file`, and `copy` modules' logic without relying on the actual system state or external services. The report generation is also tested by asserting its content against expected output based on the mocked file system.
