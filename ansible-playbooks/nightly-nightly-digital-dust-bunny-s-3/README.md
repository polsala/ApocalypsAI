# Nightly Digital Dust Bunny Sweeper

## Purpose
The "Nightly Digital Dust Bunny Sweeper" is an Ansible playbook designed to help you maintain a tidy digital workspace. It scans specified directories for files that are considered "digital dust bunnies" – files that are stale (not modified recently), empty, or don't conform to a defined naming pattern. Instead of silently accumulating digital clutter, this utility helps you identify and optionally quarantine these neglected files, keeping your repositories and knowledge bases clean and organized.

## Features
*   **Staleness Detection**: Identifies files not modified within a configurable number of days.
*   **Emptiness Check**: Flags files that are empty or below a certain size threshold.
*   **Pattern Matching**: Filters files based on a regular expression for their filenames, ensuring naming conventions are met.
*   **Report Generation**: Creates a detailed report of all identified "dust bunnies."
*   **Optional Quarantine**: Moves identified files to a designated "Digital Dust Bunny Warren" directory instead of deleting them, allowing for review.

## Usage

### Prerequisites
*   Ansible installed (version 2.9 or newer recommended).

### Setup
1.  Navigate to the `nightly-digital-dust-bunny-sweeper` directory.
2.  Review and modify `vars/main.yml` to configure your scanning preferences:
    *   `target_directory`: The directory to scan for dust bunnies.
    *   `age_threshold_days`: Files older than this will be flagged.
    *   `size_threshold_bytes`: Files smaller than this (in bytes) will be flagged.
    *   `filename_pattern`: A regex pattern for valid filenames (e.g., `^[a-zA-Z0-9_-]+\.(md|txt)$`).
    *   `quarantine_directory`: Where identified dust bunnies will be moved.
    *   `quarantine_enabled`: Set to `true` to enable quarantining, `false` to only generate a report.
    *   `report_path`: The path where the dust bunny report will be saved.

### Running the Playbook

To run the sweeper and generate a report (without quarantining, if `quarantine_enabled` is `false`):
```bash
ansible-playbook -i inventory.ini digital_dust_bunny_sweeper.yml
```

To run the sweeper and quarantine files (if `quarantine_enabled` is `true`):
```bash
ansible-playbook -i inventory.ini digital_dust_bunny_sweeper.yml
```

**Important**: It's highly recommended to run in `check_mode` first to see what changes would be made:
```bash
ansible-playbook -i inventory.ini digital_dust_bunny_sweeper.yml --check
```

### Example `vars/main.yml`
```yaml
# vars/main.yml
target_directory: "/home/user/my_notes"
age_threshold_days: 90
size_threshold_bytes: 50 # Flag files smaller than 50 bytes
filename_pattern: "^[a-zA-Z0-9_.-]+\.(md|txt|org|adoc)$" # Only allow specific extensions and characters
quarantine_directory: "/home/user/digital_dust_bunnies_quarantine"
quarantine_enabled: true
report_path: "/home/user/dust_bunny_report.txt"
```

## Automated Tests
The `tests/test_digital_dust_bunny_sweeper.yml` playbook provides a deterministic, offline test suite. It creates a mock file system structure, runs the main playbook in `check_mode`, and asserts that the expected "dust bunnies" are identified and reported correctly, without actual file modifications.

To run the tests:
```bash
ansible-playbook -i tests/inventory_test.ini tests/test_digital_dust_bunny_sweeper.yml
```
