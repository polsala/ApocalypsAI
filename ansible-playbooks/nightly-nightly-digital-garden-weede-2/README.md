# Nightly Digital Garden Weeder

Keep your digital garden tidy and free from digital weeds and pests! This Ansible playbook helps you identify and optionally prune old, unused files (weeds) and broken symbolic links (pests) across your servers. It generates a whimsical "Garden Health Report" to keep you informed.

## Features

*   **Weed Detection:** Identifies files older than a configurable threshold.
*   **Pest Control:** Finds and reports broken symbolic links.
*   **Dry Run Mode:** Safely preview changes before applying them.
*   **Customizable Paths:** Define specific directories to scan.
*   **Whimsical Reporting:** Get a clear, friendly summary of your garden's health.

## Usage

1.  **Prepare your Inventory:**
    Create an `inventory.ini` file listing the hosts where you want to run the weeder.

    ```ini
    [garden_hosts]
    your_server_1 ansible_host=192.168.1.10 ansible_user=ansible_user
    your_server_2 ansible_host=192.168.1.11 ansible_user=ansible_user
    ```

2.  **Configure the Weeder:**
    Create a `src/vars/weeder_config.yml` file to define scan paths, age thresholds, and dry-run settings.

    ```yaml
    # src/vars/weeder_config.yml
    scan_paths:
      - /var/log
      - /tmp
      - /home/ansible_user/digital_garden
    age_threshold_days: 90 # Files older than 90 days are considered weeds
    dry_run: true          # Set to 'false' to enable actual pruning/deletion
    report_path: "/tmp/digital_garden_report.txt" # Path on remote host to save the report
    ```

3.  **Run the Playbook:**
    Execute the playbook using `ansible-playbook`. Ensure you are in the `nightly-digital-garden-weeder` directory.

    ```bash
    ansible-playbook -i src/inventory.ini src/weeder.yml -e "@src/vars/weeder_config.yml"
    ```

    For a dry run (recommended initially), you can also use the `--check` flag:
    ```bash
    ansible-playbook -i src/inventory.ini src/weeder.yml -e "@src/vars/weeder_config.yml" --check
    ```

    The playbook will generate a `digital_garden_report.txt` file on each target host at the specified `report_path`.

## Example Report Output (`digital_garden_report.txt`)

```
--- Digital Garden Health Report for your_server_1 ---
Date: 2200-01-01 12:00:00

Scan Paths:
  - /var/log
  - /tmp
  - /home/ansible_user/digital_garden

Weed Age Threshold: 90 days

--- Weeds (Old Files) ---
/home/ansible_user/digital_garden/old_notes.txt
/tmp/temp_log_archive.zip

--- Pests (Broken Symlinks) ---
/home/ansible_user/digital_garden/broken_link_to_nowhere

--- Garden Status ---
Your digital garden has some weeds and pests.
Status: Dry Run (No changes were made)
```

## Development and Testing

Tests are implemented using a local Ansible playbook that sets up a mock filesystem environment, runs the weeder playbook, and asserts on the generated report. This ensures deterministic and offline testing.

To run tests:
```bash
ansible-playbook -i tests/inventory_test.ini tests/test_weeder.yml
```
