# Nightly Forage Route Optimizer

This Ansible playbook, `nightly-forage-route-optim`, helps the community manage and discover vital resources in a post-apocalyptic landscape (simulated on your servers).

It performs the following tasks:
1.  **Verifies Known Resource Caches**: Checks for the existence and integrity (permissions) of pre-defined resource locations.
2.  **Discovers New Foraging Zones**: Scans specified directories for new or recently modified files that might indicate undiscovered resources.
3.  **Generates a Foraging Manifest**: Compiles a detailed report of all known and newly discovered resources, including their status and potential value.

## Usage

1.  **Inventory**: Prepare an `inventory.ini` file listing your target servers (your 'foraging grounds').
    ```ini
    [foraging_hosts]
    server1.example.com
    server2.example.com
    ```

2.  **Configuration**: Edit `src/vars/forage_config.yml` to define your `known_caches` (paths to critical resources) and `foraging_root` (directories to scan for new finds).

    ```yaml
    # src/vars/forage_config.yml
    known_caches:
      - path: /opt/survival/water_purifier_parts.txt
        mode: '0644'
      - path: /var/lib/survival/medical_supplies/
        mode: '0755'
    foraging_root: /tmp/potential_finds
    report_path: /tmp/foraging_manifest.txt
    ```

3.  **Run the Playbook**: Execute the playbook using Ansible.
    ```bash
    ansible-playbook -i src/inventory.ini src/forage_optimizer.yml
    ```

    After execution, a `foraging_manifest.txt` (or whatever `report_path` you configured) will be generated on each target host, detailing the findings.

## Testing

To run the automated tests, ensure you have Ansible installed. The tests use a local connection to simulate target hosts and create mock files.

```bash
ansible-playbook -i tests/inventory_test.ini --connection=local tests/test_forage_optimizer.yml
```

This will:
- Create a temporary directory for mock resources.
- Simulate known caches and new finds.
- Run the main playbook against these mock resources.
- Verify the generated report content and file permissions.
- Clean up the temporary directory.
