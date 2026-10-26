# Nightly Config Blesser

This Ansible playbook ensures that specified critical configuration files on your managed hosts are "blessed" with a unique, configurable comment. This can be used to signify that a file has undergone review, is part of a sacred configuration, or simply to add a consistent header for documentation purposes.

## Features

-   **Configurable Blessing**: Define your own blessing message and the files to bless.
-   **Idempotent**: The blessing is only added if it's not already present, preventing unnecessary changes.
-   **Targeted**: Apply blessings to specific files across your inventory.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file listing your target hosts.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```

2.  **Configure the blessing**: Edit `vars/blessing_config.yml` to specify your blessing message and the paths to the files you want to bless.

    ```yaml
    ---
    blessing_message: "# Blessed by the ApocalypsAI Nightly Integrator. May its configurations be stable and its uptime eternal."
    files_to_bless:
      - /etc/nginx/nginx.conf
      - /etc/my_app/config.ini
    ```

3.  **Run the playbook**: 

    ```bash
    ansible-playbook -i src/inventory.ini src/bless_configs.yml
    ```

    To run against a specific group:
    ```bash
    ansible-playbook -i src/inventory.ini src/bless_configs.yml --limit webservers
    ```

## How it Works

The playbook iterates through `files_to_bless`. For each file, it checks if the `blessing_message` is already present at the beginning of the file. If not, it prepends the message to the file using `ansible.builtin.lineinfile` with `insertbefore: BOF`.

## Testing

This utility includes a self-contained test playbook using `ansible-playbook`'s `--check` mode and `assert` tasks to verify idempotency and correct application of the blessing.

1.  **Ensure Ansible is installed**: `pip install ansible`
2.  **Navigate to the utility directory**: `cd nightly-config-blesser`
3.  **Run the tests**:

    ```bash
    ansible-playbook -i tests/test_inventory.ini tests/test_bless_configs.yml
    ```

    The tests will:
    -   Create mock configuration files in `/tmp`.
    -   Run the `bless_configs.yml` playbook in `--check` mode on an unblessed file, expecting a change.
    -   Run the `bless_configs.yml` playbook in normal mode on the unblessed file, applying the blessing.
    -   Verify the blessing was applied by checking the file content.
    -   Run the `bless_configs.yml` playbook in `--check` mode on the now-blessed file, expecting no change (idempotency).
    -   Run the `bless_configs.yml` playbook in `--check` mode on an already blessed file, expecting no change.
    -   Clean up mock files.
