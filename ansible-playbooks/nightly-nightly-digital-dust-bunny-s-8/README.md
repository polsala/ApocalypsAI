# Nightly Digital Dust Bunny Sweeper

## Summary
This Ansible playbook helps you declutter your digital workspace by identifying and optionally cleaning up "digital dust bunnies" – old, empty, or duplicate files – across specified directories. It generates a comprehensive report, allowing you to review potential cleanup actions before committing to them.

## Features
- Identifies files older than a configurable threshold.
- Finds empty files.
- Generates a human-readable report.
- Supports a dry-run mode to preview changes without deletion.
- Configurable target directories and age thresholds.

## Prerequisites
- Ansible (version 2.9 or higher recommended)
- A system with Python installed (Ansible's control node and target node, typically `localhost` for this utility).

## Usage
1.  **Navigate to the utility directory:**
    ```bash
    cd nightly-digital-dust-bunny-sweeper
    ```

2.  **Configure your targets (optional):**
    Edit `src/vars/main.yml` to specify the `target_dirs` you want to scan, the `age_threshold_days`, and whether to run in `dry_run` mode.
    ```yaml
    # src/vars/main.yml
    target_dirs:
      - "/path/to/your/documents"
      - "/path/to/your/downloads"
    age_threshold_days: 90 # Files older than 90 days
    dry_run: true        # Set to false to actually delete files
    report_path: "/tmp/digital_dust_bunny_report.txt"
    ```

3.  **Run the playbook:**
    To perform a dry run (recommended first):
    ```bash
    ansible-playbook -i src/inventory.ini src/sweep_dust_bunnies.yml -e "dry_run=true"
    ```
    The report will be saved to the `report_path` specified in `vars/main.yml` (default: `/tmp/digital_dust_bunny_report.txt`).

    To actually delete the identified files (use with caution!):
    ```bash
    ansible-playbook -i src/inventory.ini src/sweep_dust_bunnies.yml -e "dry_run=false"
    ```

## Configuration
- `target_dirs`: A list of absolute paths to directories that the playbook should scan for dust bunnies. Default is `["/tmp/dust_bunnies_test"]` for safe initial testing.
- `age_threshold_days`: An integer representing the number of days. Files with a last modification time older than this threshold will be considered "old". Default is `30`.
- `dry_run`: A boolean (`true` or `false`). If `true`, the playbook will only report on files and will not delete anything. If `false`, it will proceed with deletion. Default is `true`.
- `report_path`: The absolute path where the generated report will be saved. Default is `"/tmp/digital_dust_bunny_report.txt"`.

## Testing
To run the automated tests, ensure you have Ansible installed and then execute:
```bash
ansible-playbook -i tests/test_inventory.ini tests/test_sweep_dust_bunnies.yml
```
This will create temporary files, run the main playbook in both dry-run and actual deletion modes, and verify its behavior. The test cleans up after itself.
