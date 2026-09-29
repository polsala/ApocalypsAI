# Nightly Comfort File Distributor

## Summary
This Ansible playbook, `nightly-comfort-file-distributo`, is designed to distribute and maintain a whimsical "comfort file" across your target servers. It ensures that every server has a `daily_comfort.txt` file in a specified directory (`/opt/comfort` by default), containing a motivational message or ASCII art, dynamically tailored with server-specific information. This utility aims to boost team morale and provides a simple, idempotent way to ensure a specific file's presence and content.

## Usage

### Prerequisites
*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions (sudo access is required for creating directories and setting file ownership/permissions in `/opt`).

### 1. Define Your Inventory
Create an `inventory.ini` file (or use an existing one) that lists your target servers. For example:

```ini
[servers]
server1.example.com
server2.example.com

[all:vars]
ansible_user=your_ssh_user
# ansible_ssh_private_key_file=~/.ssh/id_rsa
# ansible_become_pass=your_sudo_password # Only if you need password-based sudo
```

### 2. Run the Playbook
Execute the playbook using the `ansible-playbook` command:

```bash
ansible-playbook -i src/inventory.ini src/distribute_comfort_file.yml --ask-become-pass
```
(Use `--ask-become-pass` if `ansible_become_pass` is not set in inventory or vault).

### Customization
You can customize the `comfort_file_path`, `comfort_file_name`, `comfort_file_owner`, `comfort_file_group`, and `comfort_file_mode` by passing them as extra variables:

```bash
ansible-playbook -i src/inventory.ini src/distribute_comfort_file.yml \
  -e "comfort_file_path=/var/log/daily_messages" \
  -e "comfort_file_name=inspiration.log" \
  -e "comfort_file_owner=appuser" \
  -e "comfort_file_group=appgroup" \
  -e "comfort_file_mode=0600" \
  --ask-become-pass
```

You can also modify the `src/templates/comfort_file.j2` file to change the content of the comfort message. It supports Jinja2 templating, allowing dynamic content based on Ansible facts (e.g., `{{ ansible_hostname }}`, `{{ ansible_date_time.iso8601 }}`).

## Testing

To ensure the playbook works as expected and is idempotent, a dedicated test playbook is provided. This test runs locally and simulates the deployment and verification process.

### Running Tests
Navigate to the utility's root directory and execute the test playbook:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_distribute_comfort_file.yml
```

This will:
1.  Clean up any previous test artifacts.
2.  Create a temporary directory to simulate the target path.
3.  Run the main playbook in `check_mode` to verify it detects changes.
4.  Run the main playbook to apply changes.
5.  Verify the directory and file exist with correct permissions and content.
6.  Run the main playbook again to confirm idempotency (no changes reported).
7.  Clean up the temporary directory.
