# Nightly Whispering Cache Harmonizer

In the quiet hum of the post-apocalyptic night, the ApocalypsAI Nightly Integrator ensures that our vital survival caches remain in perfect harmony. The "Whispering Cache Harmonizer" is an Ansible playbook designed to gently probe your distributed resource stashes, verify their integrity, and report on any temporal discrepancies or missing provisions. It's like a digital whisper, ensuring every hidden hoard is exactly where it should be and contains what it needs.

## Features

*   **Cache Discovery**: Identifies designated survival cache locations on remote hosts.
*   **Manifest Verification**: Compares actual cache contents against a predefined `cache_manifest.yml`.
*   **Discrepancy Reporting**: Generates a detailed report highlighting missing files, unexpected items, or structural deviations.
*   **Whimsical Output**: Provides a comforting summary of cache status, ensuring peace of mind.

## Usage

1.  **Define your Inventory**:
    Create an `inventory.ini` file listing your cache servers.

    ```ini
    [cache_servers]
    cache_alpha ansible_host=your_cache_server_ip_1 ansible_user=your_user ansible_ssh_private_key_file=~/.ssh/id_rsa
    cache_beta  ansible_host=your_cache_server_ip_2 ansible_user=your_user ansible_ssh_private_key_file=~/.ssh/id_rsa
    ```

2.  **Define your Cache Manifest**:
    Edit `vars/cache_manifest.yml` to specify the desired structure and contents of your caches.

    ```yaml
    # vars/cache_manifest.yml
    cache_base_path: "/opt/survival_cache"
    required_items:
      - type: directory
        path: "rations"
      - type: directory
        path: "tools"
      - type: file
        path: "manifest.txt"
        content_regex: ".*(water|food|meds).*" # Optional: regex to check file content
      - type: file
        path: "secret_plans.txt"
    ```

3.  **Run the Harmonizer**:
    Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/harmonize_caches.yml
    ```

    To specify a custom report file path on the control node:
    ```bash
    ansible-playbook -i src/inventory.ini src/harmonize_caches.yml -e "report_file=/tmp/my_custom_harmony_report.txt"
    ```

## Example Output

The playbook will output a summary to the console and, if specified, generate a detailed report file on the control node.

```
PLAY [Whispering to Survival Caches] ******************************************

TASK [Gathering Facts] ********************************************************
ok: [cache_alpha]
ok: [cache_beta]

TASK [Check base cache path existence] ****************************************
ok: [cache_alpha]
ok: [cache_beta]

TASK [Fail if base cache path does not exist] *********************************
skipping: [cache_alpha]
skipping: [cache_beta]

TASK [Initialize cache status for cache_alpha] ********************************
ok: [cache_alpha]

TASK [Initialize cache status for cache_beta] *********************************
ok: [cache_beta]

TASK [Check if directory rations exists] **************************************
ok: [cache_alpha]
ok: [cache_beta]

TASK [Check if directory tools exists] ****************************************
ok: [cache_alpha]
failed: [cache_beta] (item={'type': 'directory', 'path': 'tools'}) => {"ansible_loop_var": "item", "changed": false, "item": {"path": "tools", "type": "directory"}, "msg": "Path /opt/survival_cache/tools does not exist"}

TASK [Check if file manifest.txt exists] **************************************
ok: [cache_alpha]
failed: [cache_beta] (item={'type': 'file', 'path': 'manifest.txt', 'content_regex': '.*(water|food|meds).*'}) => {"ansible_loop_var": "item", "changed": false, "item": {"content_regex": ".*(water|food|meds).*", "path": "manifest.txt", "type": "file"}, "msg": "Path /opt/survival_cache/manifest.txt does not exist"}

TASK [Check if file secret_plans.txt exists] **********************************
ok: [cache_alpha]
ok: [cache_beta]

PLAY [Generate Consolidated Cache Harmony Report] *****************************

TASK [Collect all cache statuses] *********************************************
ok: [localhost]

TASK [Generate report file] ***************************************************
changed: [localhost]

PLAY RECAP ********************************************************************
cache_alpha                : ok=7    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
cache_beta                 : ok=5    changed=0    unreachable=0    failed=2    skipped=1    rescued=0    ignored=0
localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Development and Testing

Tests are located in the `tests/` directory. To run them, use the provided test inventory:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_harmonized_cache.yml
ansible-playbook -i tests/inventory_test.ini tests/test_discrepant_cache.yml
```

The tests simulate various cache states on `localhost` to ensure the playbook correctly identifies and reports discrepancies, as well as correctly reports a harmonized state.
