# Nightly Digital Garden Pruner

This Ansible playbook, the "Digital Garden Pruner," helps you maintain a tidy digital space by identifying and optionally archiving or deleting old, unused files and directories. Think of it as a friendly robot gardener, gently tidying up the overgrown corners of your personal wiki, blog, or documentation repository.

## Features

*   **Age-based Pruning**: Identifies files and directories older than a specified number of days.
*   **Dry Run Mode**: Safely preview what would be pruned without making any changes.
*   **Archiving**: Moves identified items to a designated archive directory instead of immediate deletion.
*   **Configurable Paths**: Easily specify your digital garden path, archive path, and pruning age.

## Requirements

*   Ansible (version 2.9 or higher recommended)
*   Access to the target server(s) via SSH (or `localhost` for local pruning).

## Usage

1.  **Clone the repository (if not already part of it)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-digital-garden-pruner
    ```

2.  **Configure your inventory**: 
    Edit `src/inventory.ini` to specify the host(s) where your digital garden resides. For local pruning, `localhost` is sufficient.

    ```ini
    # src/inventory.ini
    [garden_servers]
    localhost ansible_connection=local
    # my_remote_server ansible_host=192.168.1.100 ansible_user=your_user
    ```

3.  **Customize variables**: 
    Edit `src/vars/main.yml` to define your garden path, the age threshold for pruning, and the archive location.

    ```yaml
    # src/vars/main.yml
    garden_path: "/path/to/your/digital/garden" # e.g., /home/user/my_notes
    prune_age_days: 90 # Items older than 90 days will be considered for pruning
    archive_path: "/path/to/your/digital/garden_archive" # Where to move old items
    dry_run: true # Set to 'false' to enable actual archiving/deletion
    ```

4.  **Run the playbook (Dry Run first!)**:
    It is **highly recommended** to run in `dry_run: true` mode first to review what will be pruned.

    ```bash
    ansible-playbook -i src/inventory.ini src/prune_garden.yml
    ```
    This will output a list of files and directories that *would* be pruned.

5.  **Perform actual pruning (if satisfied with dry run)**:
    Change `dry_run: false` in `src/vars/main.yml` and run the playbook again.

    ```bash
    ansible-playbook -i src/inventory.ini src/prune_garden.yml
    ```
    The playbook will move the identified old items to your specified `archive_path`.

## Playbook Structure

*   `src/prune_garden.yml`: The main Ansible playbook.
*   `src/inventory.ini`: Example inventory file.
*   `src/vars/main.yml`: Configuration variables for the playbook.
*   `tests/test_prune_garden.yml`: Automated tests for the playbook.

## Testing

To run the automated tests, navigate to the utility's root directory and execute:

```bash
ansible-playbook -i src/inventory.ini tests/test_prune_garden.yml
```

The tests will create a temporary digital garden, populate it with old and recent files, run the pruner in dry-run mode, and assert that the correct files are identified for pruning.
