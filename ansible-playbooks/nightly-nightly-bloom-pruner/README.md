# Nightly Bloom Pruner

## Summary

This Ansible playbook helps maintain a tidy digital garden by identifying and pruning (moving) Markdown notes that are considered 'stale' or lack an 'evergreen' tag. It's designed to prevent digital clutter and encourage focused knowledge management.

## Features

*   **Staleness Detection**: Identifies notes older than a configurable number of days.
*   **Evergreen Tagging**: Skips notes containing a specified 'evergreen' tag, preserving valuable content regardless of age.
*   **Dry Run Mode**: Safely preview which notes would be pruned without making any changes.
*   **Configurable Pruning**: Define the source directory for notes, the destination for pruned notes, and the criteria for staleness.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file (or use an existing one) that targets the host where your digital garden resides. This can be `localhost`.

    ```ini
    [garden_servers]
    localhost ansible_connection=local
    ```

2.  **Configure variables**: Adjust the `vars/main.yml` file to match your digital garden's setup.

    ```yaml
    # vars/main.yml
    notes_path: "/path/to/your/digital/garden/notes"
    prune_destination: "/path/to/your/digital/garden/archive/pruned_blooms"
    stale_age_days: 90
    evergreen_tag: "#evergreen"
    dry_run: true # Set to 'false' to perform actual pruning
    ```

3.  **Run the playbook (Dry Run first!):**

    ```bash
    ansible-playbook -i src/inventory.ini src/prune_blooms.yml
    ```

    Review the output to see which files would be pruned.

4.  **Perform actual pruning (if satisfied with dry run):**

    Change `dry_run: false` in `vars/main.yml` and run again:

    ```bash
    ansible-playbook -i src/inventory.ini src/prune_blooms.yml
    ```

## Requirements

*   Ansible (version 2.9 or higher recommended)
*   Access to the target host (e.g., `localhost` for local gardens).

## Directory Structure

```
. 
├── README.md
├── src/
│   ├── prune_blooms.yml
│   ├── inventory.ini
│   └── vars/
│       └── main.yml
└── tests/
    ├── test_prune_blooms.yml
    ├── test_inventory.ini
    └── test_vars.yml
```
