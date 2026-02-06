# Nightly MOTD Apocalypse Greeter

This Ansible playbook deploys a whimsical, apocalypse-themed Message Of The Day (MOTD) to your servers. Each login message includes a randomly selected greeting from a curated list and a summary of the server's current system status (hostname, OS, uptime, load average, and root disk usage).

## Features

- **Whimsical Greetings**: Randomly selects an apocalypse-themed greeting for each MOTD.
- **System Health Summary**: Dynamically includes key system metrics in the MOTD.
- **Idempotent**: Ensures the MOTD is always up-to-date without unnecessary changes.
- **Configurable**: Easily extendable with your own greetings and customizable MOTD path.

## Requirements

- Ansible (version 2.9 or higher recommended)
- Target servers accessible via SSH with `sudo` privileges.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file (or use an existing one) listing your target servers.

    ```ini
    # inventory.ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com
    ```

2.  **Customize Greetings (Optional)**: Edit `vars/greetings.yml` to add or modify the list of `apocalypse_greetings`.

3.  **Run the playbook**:

    ```bash
    ansible-playbook -i inventory.ini motd_greeter.yml
    ```

    To run against a specific group:

    ```bash
    ansible-playbook -i inventory.ini motd_greeter.yml --limit webservers
    ```

    To deploy to a custom path (e.g., for testing or specific use cases):

    ```bash
    ansible-playbook -i inventory.ini motd_greeter.yml -e "motd_path=/tmp/my_custom_motd"
    ```

    After running, log into one of your target servers to see the new MOTD.

## Testing

This utility includes a self-contained test playbook that uses `localhost` and mock facts to verify the MOTD generation logic without affecting your system.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_motd_greeter.yml
```

### Test Details

The `test_motd_greeter.yml` playbook:

-   Runs against `localhost` with `connection: local`.
-   Sets up mock `ansible_` facts to simulate a target host's system information.
-   Provides a fixed greeting for deterministic testing, overriding the random selection.
-   Renders the `motd.j2` template to a temporary file (`/tmp/test_motd_apocalypsai`).
-   Reads the content of the temporary file.
-   Asserts that the generated MOTD contains the expected greeting and mocked system information.
-   Cleans up the temporary file.

This approach ensures the tests are deterministic, offline, and do not require root privileges or modify the actual `/etc/motd` on the test runner.
