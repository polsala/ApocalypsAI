# Nightly Digital Garden Keeper

## Summary

The `nightly-digital-garden-keeper` is a whimsical yet practical Ansible playbook designed to cultivate and maintain a "digital garden" of files and directories on your remote hosts. It ensures that specified directories exist, "plants" new symbolic "seeds" (empty files), "waters" existing ones (updates their modification time), "prunes" old "seeds," and "weeds" empty "plots."

This utility is perfect for:
- Ensuring critical application directories and placeholder files always exist.
- Implementing a simple heartbeat mechanism by regularly touching files.
- Automating cleanup of temporary files or old logs in a controlled manner.
- Learning basic Ansible file and directory management.

## Features

- **Cultivate Plots**: Ensures specified base and sub-directories (garden plots) exist.
- **Plant Seeds**: Creates empty files (digital seeds) within plots if they don't exist.
- **Water Seeds**: Touches existing seeds to update their modification timestamp, keeping them "fresh."
- **Prune Old Seeds**: Removes seeds (files) older than a configurable number of days.
- **Weed Empty Plots**: Removes sub-directories that become empty after pruning.

## Prerequisites

- Ansible installed on your control machine.
- SSH access to your target hosts (or `ansible_connection=local` for local execution).

## Usage

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-digital-garden-keeper
    ```

2.  **Configure your inventory**:
    Edit `src/inventory.ini` to list your target hosts. For example:
    ```ini
    [garden_hosts]
    server1.example.com
    server2.example.com
    ```
    Or, for local testing:
    ```ini
    [garden_hosts]
    localhost ansible_connection=local
    ```

3.  **Configure your garden**:
    Edit `src/vars/garden_config.yml` to define your digital garden's structure and rules.
    ```yaml
    ---
    digital_garden_base_path: "/tmp/digital_garden" # Base directory for your garden
    digital_garden_plots:                           # List of sub-directories (plots)
      - "flower_beds"
      - "herb_patches"
      - "vegetable_rows"
    digital_garden_seeds_per_plot: 3                # Number of empty files (seeds) to maintain in each plot
    digital_garden_seed_prefix: "seed_"             # Prefix for seed filenames (e.g., seed_01.txt)
    digital_garden_prune_after_days: 7              # Remove seeds older than this many days
    ```

4.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/digital_garden.yml
    ```
    Add `-C` for check mode (dry run) or `-v` for verbose output.

## Automated Tests

To run the automated tests, ensure you have Ansible installed. The tests will create a temporary garden structure on your local machine, run the playbook, and then verify the state of the garden.

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_digital_garden.yml
```

The test playbook uses `delegate_to: localhost` and `connection: local` to ensure it runs deterministically without requiring remote hosts. It creates a temporary directory, simulates various garden states, runs the main playbook, and asserts the expected outcomes.
