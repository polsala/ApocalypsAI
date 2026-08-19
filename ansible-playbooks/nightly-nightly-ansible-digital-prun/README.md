# Nightly Ansible Digital Pruner

## Summary
An Ansible playbook to prune digital weeds and tidy up temporary files across your server fleet, ensuring a healthy filesystem. It targets common temporary directories and old log files, helping to maintain system hygiene and free up disk space.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file (or use an existing one) that lists the servers you want to manage.
    ```ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

2.  **Run the playbook**: Execute the playbook using `ansible-playbook`.
    ```bash
    ansible-playbook -i inventory.ini src/prune_garden.yml
    ```

3.  **Customize variables**: You can override default variables like `prune_days` (how old files must be to be pruned) and `prune_paths` (which directories to scan) by passing `--extra-vars` or defining them in a `vars/main.yml` file or directly in your inventory.
    ```bash
    ansible-playbook -i inventory.ini src/prune_garden.yml --extra-vars "prune_days=3 prune_paths=['/var/log/custom']"
    ```

## Configuration

The playbook uses the following variables, which can be overridden:

*   `prune_days`: (Default: `7`) The age in days for files to be considered for pruning. Files older than this will be removed.
*   `prune_paths`: (Default: `['/tmp', '/var/tmp', '/var/log/nginx', '/var/log/apache2', '/var/log/syslog*', '/var/log/*.log']`) A list of directories and file patterns to scan for old files.
*   `apt_cache_clean`: (Default: `true`) A boolean indicating whether to clean the APT package cache on Debian-based systems.

## Automated Tests

To ensure the Digital Pruner works as expected without affecting your live system, a dedicated test playbook is provided. It creates temporary files, runs the pruner against them, and then verifies the outcome.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_prune_garden.yml
```

This will:
1.  Create a temporary test directory and populate it with files of varying ages.
2.  Execute the `prune_garden.yml` playbook, configured to only target the test directory.
3.  Assert that old files were removed and new files were left untouched.
4.  Clean up the temporary test directory.
