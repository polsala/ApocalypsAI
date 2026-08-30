# nightly-ansible-comfort-file-distr

A whimsical Ansible playbook to ensure every server in your infrastructure receives its daily dose of digital cheer, in the form of a "comfort file" containing a motivational message or ASCII art. Because even in the apocalypse, your servers deserve a little pick-me-up!

## Features

*   **Distribute Comfort:** Places a customizable text file with a comforting message on target servers.
*   **Verification:** Checks if the comfort file exists and contains the expected content.
*   **Idempotent:** Running the playbook multiple times will only make changes if the file is missing or its content differs.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers (or `ansible_connection=local` for localhost).

### Files

*   `src/distribute_comfort.yml`: The main Ansible playbook.
*   `src/inventory.ini`: An example inventory file.
*   `src/vars/main.yml`: Variables defining the comfort message and target path.

### Configuration

Edit `src/vars/main.yml` to customize the `comfort_file_path` and `comfort_message`:

```yaml
# src/vars/main.yml
comfort_file_path: "/opt/apocalypsai/daily_comfort.txt" # Where the file will be placed
comfort_message: |
  (づ｡◕‿‿◕｡)づ
  You're doing great!
  Keep up the good work,
  even in the apocalypse.
  The void appreciates you.
```

### Running the Playbook

1.  **Update your inventory:** Modify `src/inventory.ini` to include your target servers.
    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com

    [local]
    localhost ansible_connection=local
    ```
2.  **Execute the playbook:**
    ```bash
    ansible-playbook -i src/inventory.ini src/distribute_comfort.yml
    ```

    To run against a specific group (e.g., `webservers`):
    ```bash
    ansible-playbook -i src/inventory.ini src/distribute_comfort.yml --limit webservers
    ```

## Testing

The utility includes a self-contained test playbook that runs against `localhost`.

To run the tests:

```bash
ansible-playbook -i src/inventory.ini tests/test_distribute_comfort.yml
```

This will:
1.  Define test-specific variables for the comfort file path and content.
2.  Clean up any previous test artifacts.
3.  Execute the `src/distribute_comfort.yml` playbook against `localhost` using the test variables.
4.  Verify that the comfort file was created at the expected path and contains the correct content.
5.  Clean up the test comfort file.

## Contributing

Feel free to suggest new comfort messages, alternative distribution methods, or additional verification steps!
