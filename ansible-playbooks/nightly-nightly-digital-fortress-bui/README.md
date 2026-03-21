# Nightly Digital Fortress Builder

This Ansible playbook, `nightly-digital-fortress-builder`, is designed to establish a foundational layer of security on your Linux servers. It automates essential hardening steps, transforming your systems into robust digital fortresses against common threats.

## Features

*   **System Updates**: Ensures your system's package cache is updated and all packages are upgraded.
*   **Firewall Configuration**: Installs and configures `ufw` (Uncomplicated Firewall) to deny all incoming traffic by default, while allowing essential services like SSH (on a configurable port), HTTP, and HTTPS.
*   **Intrusion Prevention**: Installs `fail2ban` to protect against brute-force attacks.
*   **SSH Hardening**: Modifies `sshd_config` to:
    *   Disable root login.
    *   Optionally disable password authentication (relying on SSH keys).
    *   Ensure empty passwords are not permitted.
    *   Limit maximum authentication attempts.

## Prerequisites

*   **Ansible**: Installed on your control machine.
*   **Target Servers**: Linux servers (tested on Debian/Ubuntu-based systems) accessible via SSH.
*   **Sudo Privileges**: The Ansible user on the target servers must have `sudo` privileges without requiring a password (or you will be prompted).
*   **SSH Keys**: If `disable_password_auth` is set to `true` in `vars/fortress_config.yml`, ensure you have SSH key-based authentication set up for your target servers.

## Usage

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-digital-fortress-builder
    ```

2.  **Configure your inventory**: Edit `src/inventory.ini` to list your target servers. For example:
    ```ini
    [fortress_servers]
    your_server_ip_1 ansible_user=your_user
    your_server_ip_2 ansible_user=your_user
    ```
    For local testing, you can use:
    ```ini
    [fortress_servers]
    localhost ansible_connection=local
    ```

3.  **Customize variables (optional)**: Review and modify `vars/fortress_config.yml` to adjust settings like the SSH port or whether to disable password authentication.
    ```yaml
    # vars/fortress_config.yml
    ssh_port: 22
    disable_password_auth: true # Set to false if you still need password auth
    ```

4.  **Run the playbook**: Execute the playbook using `ansible-playbook`:
    ```bash
    ansible-playbook -i src/inventory.ini src/fortress_builder.yml --ask-become-pass
    ```
    (Remove `--ask-become-pass` if your user has passwordless sudo configured.)

5.  **Verify**: After the playbook runs, you can manually verify the changes on your server:
    *   Check UFW status: `sudo ufw status verbose`
    *   Check SSH config: `sudo grep -E 'PermitRootLogin|PasswordAuthentication|PermitEmptyPasswords|MaxAuthTries' /etc/ssh/sshd_config`

## Testing

To run the automated tests for this playbook, which verify its idempotency and correct SSH configuration changes in an isolated, offline manner:

```bash
ansible-playbook -i src/inventory.ini tests/test_fortress_builder.yml
```

These tests create a temporary `sshd_config` file, apply the playbook's SSH hardening tasks to it, and then assert the final content and idempotency without affecting your actual system configuration.
