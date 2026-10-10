# Nightly Server Serenity Enforcer

The `nightly-server-serenity-enforcer` is an Ansible playbook designed to infuse your servers with a touch of whimsical calm and ensure a consistently comforting digital environment. It sets a welcoming Message Of The Day (MOTD), installs classic feel-good command-line utilities (`cowsay` and `fortune`), and schedules a daily dose of wisdom delivered by a talking animal.

Because even in the post-apocalypse, your servers deserve a little zen.

## Features

- **Custom MOTD**: Sets a friendly and comforting message upon login.
- **Whimsical Utilities**: Installs `cowsay` and `fortune-mod` for delightful terminal interactions.
- **Daily Wisdom**: Schedules a cron job to display a random fortune via `cowsay` every morning.

## Usage

### Prerequisites

- Ansible installed on your control machine.
- SSH access to your target servers (or `localhost` for local execution).
- Python 3 on target servers (for Ansible's `raw` module if needed, though `package` and `copy` are usually fine).

### Running the Playbook

1.  **Navigate to the utility directory**:
    ```bash
    cd nightly-server-serenity-enforcer
    ```

2.  **Edit `src/inventory.ini`**:
    Specify your target servers. For local execution, `localhost` is already configured.
    ```ini
    [serene_servers]
    # Replace with your server IPs or hostnames
    # server1.example.com
    # server2.example.com
    localhost ansible_connection=local
    ```

3.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/serenity_enforcer.yml
    ```
    This will apply the serenity configurations to your specified hosts.

## Testing

To ensure the serenity enforcer has done its job, you can run the included test playbook.

1.  **Ensure the main playbook has been run at least once** to set up the environment.
    ```bash
    ansible-playbook -i src/inventory.ini src/serenity_enforcer.yml
    ```

2.  **Run the test playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini tests/test_serenity_enforcer.yml
    ```

    If all checks pass, you will see output indicating success for each task. If any task fails, it means a component of the serenity setup is missing or incorrectly configured.

### Deterministic & Offline Testing Rationale

The tests are designed to be deterministic and run offline (or against `localhost` without external dependencies).
-   **Package Checks (`command -v cowsay`, `command -v fortune`)**: These commands verify the presence of executables on the target system. They are deterministic as `command -v` will consistently report if a command exists in the PATH.
-   **MOTD Content Check (`cat /etc/motd`)**: This reads a local file. Its output is deterministic based on the file's content, which is set by the main playbook.
-   **Script Existence/Executability (`stat`)**: The `ansible.builtin.stat` module checks local file system properties. This is deterministic and doesn't involve external calls.
-   **Cron Job Check (`cron` module with `check_mode`)**: The `ansible.builtin.cron` module, when run with `check_mode: yes`, will report whether a change *would* be made to the crontab to achieve the desired state. If `changed: false` is reported, it means the cron job is already in the desired state, making this a deterministic verification without actual modification.

These tests ensure that the playbook's effects are verifiable and consistent across runs, without relying on external network services or dynamic data.
