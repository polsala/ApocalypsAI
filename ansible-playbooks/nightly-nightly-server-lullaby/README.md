# Nightly Server Lullaby

## Summary
This Ansible playbook, `nightly-server-lullaby`, is designed to provide a gentle, nightly maintenance routine for your servers. It performs essential tasks like updating package caches and cleaning up old packages, followed by setting a whimsical "lullaby" Message of the Day (MOTD) to remind everyone that the server is in a peaceful, well-maintained state.

## Features
- **Gentle Maintenance**: Updates package lists and cleans up old packages (supports Debian/Ubuntu and RedHat/CentOS).
- **Whimsical MOTD**: Sets a custom, calming Message of the Day to reflect the server's rested state.
- **Idempotent**: Can be run multiple times without causing unintended side effects.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access to your target servers with appropriate privileges (or `ansible_connection=local` for localhost).

### Files
- `src/lullaby.yml`: The main Ansible playbook.
- `src/inventory.ini`: An example inventory file.
- `src/vars/lullaby_config.yml`: Variables for customizing the MOTD content.

### Running the Playbook
1.  **Define your inventory**: Edit `src/inventory.ini` to include the servers you wish to manage. For local testing, `localhost ansible_connection=local` is pre-configured.

    ```ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

2.  **Customize MOTD (Optional)**: Modify `src/vars/lullaby_config.yml` to change the `motd_content` variable if desired.

    ```yaml
    motd_content: |
      ******************************************************************
      *                                                                *
      *   Shhh... the server is dreaming of efficient processes and    *
      *   bug-free code. Please tread lightly.                         *
      *                                                                *
      *   Last Lullaby: {{ ansible_date_time.iso8601_basic_short }}    *
      *                                                                *
      ******************************************************************
    ```

3.  **Run the playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/lullaby.yml
    ```

    To perform a dry run (check mode) without making any changes:

    ```bash
    ansible-playbook -i src/inventory.ini src/lullaby.yml --check --diff
    ```

## Testing

This utility includes a self-contained test playbook to verify its syntax and execution flow in check mode.

### Running Tests
1.  Ensure Ansible is installed on the machine where you are running the tests.
2.  Execute the test playbook:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_lullaby.yml
    ```

This test will:
- Attempt to install Ansible locally if not present (for the test runner).
- Run the `lullaby.yml` playbook in `--syntax-check --check --diff` mode.
- Assert that the check run completes without errors.
- Verify that the `motd_content` variable is correctly defined and contains expected whimsical phrases.

### Mock Rationale
- The test uses `ansible.builtin.command` to execute the main playbook in check mode, verifying its operational integrity without actual system modification.
- Assertions on `check_output.rc` and `stdout` ensure the playbook's syntax is valid and it can be processed by Ansible.
- The `motd_content` variable is directly asserted to confirm its structure and content, simulating the expected output without writing to `/etc/motd`.
- Actual package management operations (apt/yum) are not performed during the test, adhering to the deterministic and offline requirement. Their presence and conditional execution are implicitly verified by the playbook running successfully in check mode.
