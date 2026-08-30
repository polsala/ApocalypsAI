# Nightly Survival Cache Verifier

## Summary
This Ansible playbook is designed to verify the integrity of critical "survival cache" files across your designated servers. It uses SHA256 checksums to detect any unauthorized modifications, corruption, or missing files, ensuring your essential configurations, scripts, or data backups remain in their pristine, expected state.

## Whimsical Context
In the post-apocalyptic digital wasteland, your servers are your shelters, and their configurations are your survival kits. This utility acts as a vigilant guardian, constantly checking that no digital raiders (or accidental keystrokes) have tampered with your precious resources. Keep your digital provisions safe and sound!

## Usage
1.  **Define your inventory**: Create an `inventory.ini` file (or use an existing one) that lists the servers where your survival cache files reside.
    ```ini
    [shelter_servers]
    server1.example.com
    server2.example.com

    [all:vars]
    ansible_user=your_ssh_user
    ansible_ssh_private_key_file=~/.ssh/id_rsa
    ```

2.  **Define your survival cache manifest**: Populate `src/vars/cache_manifest.yml` with the absolute paths of the files you want to monitor and their *expected* SHA256 checksums. You can generate checksums using `sha256sum /path/to/file` on a known good version of the file.
    ```yaml
    # src/vars/cache_manifest.yml
    survival_cache_files:
      "/etc/survival_kit/main_config.conf": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
      "/opt/critical_scripts/launch_sequence.sh": "da39a3ee5e6b4b0d3255bfef95601890afd80709"
      "/var/lib/data/backup_manifest.json": "f29bc64d4d1265881023793739722364c76045952972986877e6820251411a76"
    ```

3.  **Run the playbook**: Execute the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i src/inventory.ini src/verify_cache.yml
    ```
    The playbook will connect to each server, calculate the SHA256 checksum for each specified file, compare it against your manifest, and report the integrity status. If any file fails the check, the playbook will fail, indicating a potential issue.

## Prerequisites
*   Ansible installed on your control machine.
*   Python installed on all target hosts (managed nodes).
*   SSH access to target hosts configured for your Ansible user.

## Automated Tests
To run the automated tests for this utility:
```bash
ansible-playbook -i tests/inventory_test.ini tests/test_verify_cache.yml
```
This will execute a local test scenario that creates dummy files, tampers with one, and checks for a missing file, then asserts that the `verify_cache.yml` playbook correctly identifies the integrity status of each.
