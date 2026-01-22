# Nightly Cache Keeper

## Summary

In the ever-shifting landscape of the apocalypse, maintaining the integrity of your distributed survival caches is paramount. The `Nightly Cache Keeper` is an Ansible playbook designed to ensure that your designated cache locations across various hosts (or even locally) maintain a consistent directory structure, correct permissions, and a placeholder manifest file. It's like a digital guardian for your hidden stashes, ensuring they're always ready for when you need them most.

## Usage

1.  **Prerequisites**:
    *   Ansible installed (version 2.10 or higher recommended).
    *   Python 3 on the control node and target hosts.

2.  **Inventory Setup**:
    Create an `inventory.ini` file (or modify the provided example) listing the hosts where your survival caches are located. For local testing or single-machine management, `localhost` is sufficient.

    ```ini
    [caches]
    localhost ansible_connection=local
    # Add other hosts here, e.g.:
    # remote_cache_server ansible_host=192.168.1.10 ansible_user=survivor
    ```

3.  **Configure Variables**:
    Edit `vars/main.yml` to define your `cache_base_path`, `cache_locations`, desired `owner`, `group`, `mode`, and the content for your `manifest_filename`.

    ```yaml
    ---
    cache_base_path: "/tmp/apocalypsai_caches" # Base directory for all caches
    cache_locations:
      - "food_stash"
      - "water_reserve"
      - "tool_depot"
    cache_owner: "{{ ansible_user_id | default('root') }}" # Owner of the cache directories
    cache_group: "{{ ansible_user_gid | default('root') }}" # Group of the cache directories
    cache_mode: "0755" # Permissions for the cache directories (octal string)
    manifest_filename: "cache_manifest.txt"
    manifest_content: |
      # ApocalypsAI Cache Manifest
      # This file ensures the cache structure is maintained.
      # Add your actual inventory here.
      - Item A: 5 units
      - Item B: 10 units
    ```

4.  **Run the Playbook**:
    Execute the playbook using the `ansible-playbook` command:

    ```bash
    ansible-playbook -i inventory.ini cache_keeper.yml
    ```

    To perform a dry run without making changes, use the `--check` flag:

    ```bash
    ansible-playbook -i inventory.ini cache_keeper.yml --check
    ```

## Testing

To ensure the `Nightly Cache Keeper` is functioning as expected, a dedicated test playbook is provided. This test playbook will:

1.  Clean up any existing test artifacts.
2.  Run the main `cache_keeper.yml` playbook.
3.  Verify that the base cache path, individual cache directories, and manifest files exist with the correct permissions and content.

To run the tests:

```bash
ansible-playbook -i tests/tests_inventory.ini tests/test_cache_keeper.yml
```

**Note**: The tests are designed to run on `localhost` and will create/remove directories under the `cache_base_path` defined in `vars/main.yml` (defaulting to `/tmp/apocalypsai_caches`). Ensure you have appropriate permissions or run with `sudo` if necessary (the playbook uses `become: yes`).
