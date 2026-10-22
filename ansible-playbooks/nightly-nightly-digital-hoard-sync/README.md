# Nightly Digital Hoard Sync

## Summary
This Ansible playbook ensures your critical 'digital hoard' – essential files, configurations, and scripts – are consistently synchronized to designated 'bunker' or survival servers. It's designed for maintaining the integrity and availability of your most vital digital assets in a post-apocalyptic or disaster recovery scenario.

## How it Works
1.  **Configuration**: Define your digital hoard items (source paths and their desired destinations) in `vars/hoard_config.yml`.
2.  **Inventory**: Specify your target 'bunker' servers in `src/inventory.ini`.
3.  **Synchronization**: The playbook uses Ansible's `synchronize` module (which leverages `rsync` under the hood) to efficiently copy and update files and directories from the Ansible controller to the target servers.
4.  **Idempotency**: The playbook is idempotent, meaning running it multiple times will achieve the same desired state without making unnecessary changes.

## Prerequisites
*   **Ansible**: Installed on your control machine.
*   **SSH Access**: Passwordless SSH access (via keys) from your control machine to all target 'bunker' servers.
*   **Python**: Python interpreter available on target servers (usually pre-installed).
*   **Rsync**: `rsync` utility installed on both the control machine and target servers for efficient synchronization.

## Usage
1.  **Clone the repository** (if not already part of your ApocalypsAI setup).
2.  **Navigate** to the `nightly-digital-hoard-sync` directory.
3.  **Configure your hoard**: Edit `vars/hoard_config.yml` to specify the files and directories you want to synchronize.
    *   `base_src_path`: The base directory on the Ansible controller where your hoard items are located.
    *   `base_dest_path`: The base directory on the target servers where the hoard items should be placed.
    *   `digital_hoard_items`: A list of dictionaries, each with `src` (relative to `base_src_path`) and `dest` (relative to `base_dest_path`).
4.  **Update your inventory**: Modify `src/inventory.ini` to list your target servers under the `[bunker_servers]` group.
5.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/sync_hoard.yml
    ```

## Example `vars/hoard_config.yml`
```yaml
---
base_src_path: "/path/to/your/local/hoard"
base_dest_path: "/opt/apocalypsai/hoard"
digital_hoard_items:
  - src: "essential_scripts/"
    dest: "scripts/"
  - src: "configs/server.conf"
    dest: "configs/server.conf"
  - src: "important_docs/survival_guide.txt"
    dest: "docs/survival_guide.txt"
```

## Testing
To run the included tests, ensure Ansible is installed and execute:
```bash
ansible-playbook -i src/inventory.ini tests/test_sync_hoard.yml
```
This will simulate the synchronization process on `localhost` and verify its correctness and idempotency.
