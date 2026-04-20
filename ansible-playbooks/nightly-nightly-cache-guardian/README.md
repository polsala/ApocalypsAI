# ApocalypsAI Nightly Cache Guardian

This Ansible playbook, the "Nightly Cache Guardian," is designed to help maintain the integrity and readiness of your distributed survival caches. In a world of temporal anomalies and unpredictable events, ensuring your hidden stashes are untouched and periodically "blessed" with fresh temporal energy (or just a new timestamp) is paramount.

## Features

*   **Cache Path Management**: Ensures the base directory for your caches exists on target hosts.
*   **Manifest Verification**: Checks for the presence of a `cache_manifest.txt` file in each designated cache location, indicating its existence and initial setup.
*   **Integrity Check**: Calculates SHA256 checksums for a `temporal_blessing.txt` file within each cache, allowing you to detect tampering or drift.
*   **Temporal Blessing**: Creates or updates a `temporal_blessing.txt` file in each cache with a random "survival mantra" and a current timestamp, simulating a periodic refresh or re-blessing of the cache.
*   **Report Generation**: Generates a `cache_guardian_report_<hostname>.txt` on each target host, summarizing the status of all managed caches.

## Usage

1.  **Define your inventory**: Edit `inventory.ini` to list your cache servers or `localhost` for local testing.
    ```ini
    [caches]
    localhost ansible_connection=local
    # cache_server_1
    # cache_server_2
    ```

2.  **Configure cache details**: Modify `vars/main.yml` to specify the `cache_base_path`, `cache_locations`, `manifest_filename`, `blessing_filename`, and the `blessing_messages`.
    ```yaml
    # vars/main.yml
    cache_base_path: "/opt/apocalypsai_caches" # Or /tmp/apocalypsai_caches for testing
    cache_locations:
      - "sector_alpha_stash"
      - "sector_beta_vault"
      - "sector_gamma_hideout"
    manifest_filename: "cache_manifest.txt"
    blessing_filename: "temporal_blessing.txt"
    blessing_messages:
      - "May your rations be plentiful and your spirits unyielding."
      - "The void whispers, but resilience echoes louder."
      - "Hope is the last resource, guard it well."
      - "In the darkest night, remember the dawn."
    ```

3.  **Run the playbook**: Execute the main playbook.
    ```bash
    ansible-playbook -i inventory.ini cache_guardian.yml
    ```

    *   To run in check mode (dry run):
        ```bash
        ansible-playbook -i inventory.ini cache_guardian.yml --check
        ```

4.  **Review reports**: After execution, check the `cache_base_path` on each target host for the generated `cache_guardian_report_<hostname>.txt` files.

## Testing

To ensure the Nightly Cache Guardian is functioning correctly, a dedicated test playbook is provided. This test creates a temporary environment, runs the guardian, and asserts the expected outcomes.

To run the tests:

```bash
ansible-playbook -i inventory.ini tests/test_cache_guardian.yml
```

This will:
1.  Clean up any previous test artifacts.
2.  Set up a temporary cache base path (`/tmp/apocalypsai_test_caches`).
3.  Create dummy cache locations and manifest files.
4.  Run the main `cache_guardian.yml` playbook in check mode and assert that no actual changes (like blessing file creation) occur.
5.  Run the main `cache_guardian.yml` playbook for real.
6.  Verify that blessing files were created with the expected content.
7.  Verify manifest files still exist.
8.  Verify a report file was generated.
9.  Clean up the temporary test environment.
