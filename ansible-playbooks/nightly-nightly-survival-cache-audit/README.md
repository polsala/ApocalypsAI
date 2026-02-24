### Nightly Survival Cache Auditor

This Ansible playbook automates the auditing of critical files and directories across your survival infrastructure. It ensures that essential files are present, have correct permissions, and optionally match expected checksums, providing a vital check on the integrity of your survival caches.

#### Features:
- Verifies existence of files and directories.
- Checks file/directory permissions (mode).
- Validates owner and group.
- Optionally compares SHA256 checksums for files.
- Generates a detailed audit report.
- Supports marking items as optional, so their absence doesn't trigger a failure.

#### Usage:

1.  **Define your inventory**: Create or update `src/inventory.ini` with the hosts you want to audit.
    ```ini
    [survival_hosts]
    your_server_1
    your_server_2
    # localhost ansible_connection=local # For local testing
    ```

2.  **Configure your survival cache manifest**: Edit `src/vars/cache_manifest.yml` to specify the items to audit.

    Each item can have the following properties:
    -   `path`: (Required) The absolute path to the file or directory.
    -   `state`: (Required) `"file"` or `"directory"`.
    -   `mode`: (Optional) Expected file/directory permissions (e.g., `"0644"`, `"0700"`).
    -   `owner`: (Optional) Expected owner username (e.g., `"root"`, `"ansible_user_id"`).
    -   `group`: (Optional) Expected group name (e.g., `"root"`, `"ansible_user_gid"`).
    -   `checksum`: (Optional) Expected SHA256 checksum (e.g., `"sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"` for an empty file).
    -   `optional`: (Optional) Set to `true` if the item's absence should not cause a failure. Defaults to `false`.
    -   `description`: (Optional) A human-readable description of the item.

    Example `src/vars/cache_manifest.yml`:
    ```yaml
    ---
    survival_cache_items:
      - path: "/opt/survival_kit/emergency_manual.txt"
        state: "file"
        mode: "0644"
        owner: "root"
        group: "root"
        checksum: "sha256:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
        description: "The essential emergency survival manual."
      - path: "/var/log/survival_events"
        state: "directory"
        mode: "0755"
        owner: "syslog"
        group: "adm"
        description: "Log directory for critical survival events."
      - path: "/etc/survival_config/optional_settings.conf"
        state: "file"
        optional: true
        description: "Optional configuration file, may not be present on all hosts."
    ```

3.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/audit_cache.yml
    ```

    The playbook will generate an audit report in `/tmp/survival_cache_audit_report_YYYYMMDDTHHMMSS.txt` on the machine where Ansible is run.

#### Running Tests:

To run the included tests, ensure you have Ansible installed. The tests use `localhost` and create temporary files to simulate various audit scenarios.

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_audit_cache.yml
```

This will:
1.  Create a temporary directory and mock files with specific properties.
2.  Run the `audit_cache.yml` playbook against these mock files.
3.  Assert that the audit results match the expected `PASS`/`FAIL` outcomes for each scenario.
4.  Clean up the temporary files and generated report.
