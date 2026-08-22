# Nightly Ansible Digital Garden Sync

This Ansible playbook helps you maintain your "digital garden" – a collection of personal notes, knowledge base articles, or markdown files – across multiple machines. It ensures your garden is synchronized, regularly backed up, and helps you identify notes that might be growing a bit too stale.

## Features

*   **Synchronization**: Pushes your digital garden files from a central source (your Ansible control node) to all specified managed hosts.
*   **Backup**: Creates a timestamped archive of your digital garden on each managed host for disaster recovery.
*   **Stale Note Detection**: Identifies files that haven't been modified in a configurable number of days, prompting you to review or prune them.

## How it Works

The playbook performs the following steps on each target host:

1.  Ensures the target directory for your digital garden exists.
2.  Uses the `synchronize` module to push files from your local `garden_source_path` to the remote `garden_target_path`.
3.  Ensures a backup directory exists.
4.  Creates a gzipped tar archive of the `garden_target_path` in the `garden_backup_path` with a timestamp.
5.  Scans the `garden_target_path` for files older than `stale_days` (based on modification time) and reports them.

## Usage

1.  **Install Ansible**: If you don't have Ansible installed, follow the official documentation.
2.  **Clone this utility**: Place the `nightly-ansible-digital-garden-sync` folder in your Ansible project.
3.  **Configure Inventory**: Create an `inventory.ini` file (or modify the provided `src/inventory.ini`) listing your target hosts where the digital garden should reside.
4.  **Configure Variables**: Adjust the variables in `src/vars/main.yml` to match your setup.
5.  **Run the Playbook**:

    ```bash
    ansible-playbook -i src/inventory.ini src/sync_garden.yml
    ```

### Example `src/inventory.ini`

```ini
[garden_hosts]
localhost ansible_connection=local
# my_laptop.local
# my_server.example.com
```

### Example `src/vars/main.yml`

```yaml
garden_source_path: "/path/to/your/local/garden" # Path on the Ansible control node
garden_target_path: "/home/user/my_notes"      # Path on the managed nodes
garden_backup_path: "/var/backups/notes"       # Backup path on managed nodes
stale_days: 90                                 # Number of days after which a note is considered stale
```

## Variables

*   `garden_source_path`: **(Required)** The absolute path to your digital garden directory on the Ansible control node. This is the source of truth.
*   `garden_target_path`: **(Required)** The absolute path on the managed hosts where the digital garden files will be synchronized.
*   `garden_backup_path`: **(Required)** The absolute path on the managed hosts where timestamped backups will be stored.
*   `stale_days`: **(Optional, default: 90)** The number of days after which a file's modification time (`mtime`) will flag it as "stale".

## Testing

The utility includes a self-contained test playbook (`tests/test_sync_garden.yml`) that can be run locally to verify its functionality without affecting your actual files. It creates temporary directories and mock files, runs the main playbook, and asserts the outcomes.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_sync_garden.yml
```
