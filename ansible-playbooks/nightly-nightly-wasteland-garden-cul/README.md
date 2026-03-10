# Nightly Wasteland Garden Cultivator

This Ansible playbook helps you cultivate your digital 'wasteland gardens' by ensuring that critical directories and placeholder files are present on your servers with the correct permissions and ownership. Think of it as preparing fertile ground for your post-apocalyptic data.

## Features

*   **Directory Creation**: Ensures specified directories exist.
*   **File Placement**: Creates placeholder files within these directories, optionally with initial content.
*   **Permission Enforcement**: Sets precise file and directory modes (permissions) and ownership.
*   **Idempotent**: Can be run multiple times without causing unintended changes.

## Prerequisites

*   **Ansible**: Installed on your control machine.
*   **SSH Access**: To your target servers (if not running locally).
*   **Sudo/Become Privileges**: The playbook uses `become: yes` to manage system-level directories and permissions.

## Usage

1.  **Define your Inventory**: Create an `inventory.ini` file listing your target servers. For local testing, you can use `localhost`.

    ```ini
    # src/inventory.ini
    [wasteland_servers]
    localhost ansible_connection=local
    # other_server_1
    # other_server_2
    ```

2.  **Configure your Garden**: The `garden_config` variable in `src/cultivate_garden.yml` defines the paths, states (directory), modes, owners, groups, and any initial files to be created. You can override this variable via `--extra-vars` or by creating a `vars/main.yml` file.

    Example `garden_config` structure:

    ```yaml
    garden_config:
      - path: "/opt/wasteland_resources"
        state: directory
        mode: "0755"
        owner: "root"
        group: "root"
        files:
          - name: "scavenged_data.log"
            content: "Initial log entry\n"
            mode: "0644"
          - name: ".resource_marker"
            content: ""
            mode: "0600"
      - path: "/var/lib/settlement_cache"
        state: directory
        mode: "0770"
        owner: "ansible_user" # Replace with actual user/group if not root
        group: "ansible_group"
        files: []
    ```

3.  **Run the Playbook**:

    Navigate to the `nightly-wasteland-garden-cultivator` directory and execute:

    ```bash
    ansible-playbook -i src/inventory.ini src/cultivate_garden.yml
    ```

    To run with specific variables (e.g., for testing or custom configurations):

    ```bash
    ansible-playbook -i src/inventory.ini src/cultivate_garden.yml \
      --extra-vars '{"garden_config": [{"path": "/tmp/my_test_garden", "state": "directory", "mode": "0700", "files": []}]}'
    ```

## Testing

The `tests/test_cultivate_garden.yml` playbook provides a self-contained, deterministic test suite. It runs the main playbook against `localhost` in a temporary directory and verifies the creation and permissions of directories and files.

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_cultivate_garden.yml
```

This will create a temporary directory (e.g., `/tmp/ansible_test_garden_1678888888`), run the cultivation tasks within it, verify the results, and then clean up the temporary directory.
