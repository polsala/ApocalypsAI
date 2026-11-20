# Nightly Ansible Digital Guardian Deploy

## Summary
This Ansible playbook, `nightly-ansible-guardian-deploy`, is designed to deploy and configure essential 'guardian' services on your target servers. It ensures that critical security and maintenance tools like `fail2ban` and `unattended-upgrades` are installed, properly configured, and actively vigilant, protecting your digital realm.

## What it Does
-   **Installs Guardian Packages**: Ensures `fail2ban` and `unattended-upgrades` are installed.
-   **Configures Fail2Ban**: Sets up `fail2ban` to protect SSH access with a default jail configuration.
-   **Configures Unattended Upgrades**: Enables automatic security updates and reboots for continuous system health.
-   **Ensures Service Vigilance**: Verifies that `fail2ban` and `unattended-upgrades` services are running and enabled.
-   **Generates Vigil Report**: Creates a whimsical 'Digital Guardian Vigil Report' on the Ansible controller, summarizing the status of the deployed guardians and their configurations.

## Usage

### Prerequisites
-   Ansible installed on your control machine.
-   SSH access to your target servers with `sudo` privileges.

### 1. Inventory Setup
Create an `inventory.ini` file (or modify the provided `src/inventory.ini`) listing your target servers under the `[guardians]` group. For local testing, `localhost` is included.

```ini
# src/inventory.ini
[guardians]
localhost ansible_connection=local
# server1.example.com
# server2.example.com
```

### 2. Run the Playbook
Execute the playbook from the root of this utility's directory:

```bash
ansible-playbook -i src/inventory.ini src/deploy_guardians.yml
```

After execution, a report will be generated at `/tmp/digital_guardian_vigil_report.txt` on your Ansible control machine.

## Automated Tests

To ensure the playbook functions as expected without making actual changes to your system, a test playbook is provided. It uses Ansible's `check_mode` and mocks certain facts to verify the playbook's logic and template rendering.

### Running Tests
From the root of this utility's directory, execute the test playbook:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_deploy_guardians.yml
```

This will:
1.  Run the main `deploy_guardians.yml` playbook in `check_mode` against `localhost`.
2.  Assert that the playbook *would* make the necessary changes (install packages, configure files, start services).
3.  Render the `guardian_report.j2` template with mocked data to ensure its output format is correct.
4.  Assert the content of the generated report matches expected values.

**Note**: The tests are designed to be deterministic and offline. `check_mode` simulates changes without applying them, and specific facts are mocked for template rendering to ensure consistent test results.
