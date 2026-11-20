# Nightly Digital Garden Pruner

## Overview
The `nightly-digital-garden-pruner` is an Ansible playbook designed to bring a touch of whimsy to server maintenance. It simulates the 'pruning' of a digital garden by restarting specified services (to refresh them) and clearing designated log files (to prevent overgrowth). After its work, it generates a 'pruning report' detailing the actions taken, ensuring your digital flora remains vibrant and healthy.

## Features
- **Service Refresh**: Restarts critical or designated services to keep them 'fresh'.
- **Log Clearing**: Empties specified log files to prevent disk space 'overgrowth'.
- **Pruning Report**: Generates a timestamped report summarizing all pruning activities.
- **Configurable**: Easily define which services to restart and which logs to clear via `vars/garden_config.yml`.

## Setup
1.  **Install Ansible**: If you don't have Ansible installed, follow the official documentation: `pip install ansible`.
2.  **Navigate**: Change into the `nightly-digital-garden-pruner` directory.

## Usage
1.  **Configure your Garden**: Edit `src/vars/garden_config.yml` to specify the `pruning_report_dir`, `log_files_to_clear`, and `services_to_restart` according to your needs. For services, you'll specify a `restart_marker_path` which the playbook will `touch` to simulate a restart (for testing purposes, or if you adapt it to use actual service modules).
2.  **Prepare Inventory**: Ensure your `src/inventory.ini` lists the hosts you want to prune. For local testing, `localhost` with `ansible_connection=local` is sufficient.
3.  **Run the Pruner**: Execute the playbook:
    ```bash
    ansible-playbook -i src/inventory.ini src/prune_garden.yml
    ```
    The playbook will perform the configured actions and generate a report in the specified `pruning_report_dir`.

## Testing
To ensure the Digital Garden Pruner is working as expected, run the included test playbook:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_prune_garden.yml
```

This test playbook will:
1.  Clean up any previous test artifacts.
2.  Create mock log files with content and mock service marker files.
3.  Run the main `prune_garden.yml` playbook.
4.  Verify that log files are cleared (empty).
5.  Verify that service marker files have updated timestamps (simulating restarts).
6.  Assert that a pruning report was generated and contains the expected summary of actions.

All tests are designed to be deterministic and run offline against `localhost` by simulating file system changes and checking their state.
