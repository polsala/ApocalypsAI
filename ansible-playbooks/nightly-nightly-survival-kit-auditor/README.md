# Nightly Survival Kit Auditor

Ensuring your digital infrastructure is prepared for any eventuality is paramount. The `Nightly Survival Kit Auditor` is an Ansible playbook designed to scan your target servers for a predefined set of essential software packages and critical configuration files. Think of it as a pre-apocalyptic readiness check for your systems!

## Features

*   **Package Presence Check**: Verifies if a list of specified packages are installed.
*   **Configuration File Check**: Confirms the existence of critical configuration files.
*   **Detailed Reporting**: Provides a summary of missing packages and files.
*   **Customizable**: Easily define your own "survival kit" via `vars/survival_kit.yml`.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers (or `ansible_connection=local` for localhost).

### 1. Define your Inventory

Create an `inventory.ini` file (or use an existing one) listing your target servers.

```ini
[survival_servers]
server1.example.com
server2.example.com ansible_user=ubuntu
```

### 2. Customize Your Survival Kit

Edit `vars/survival_kit.yml` to specify the packages and files you consider essential.

```yaml
# vars/survival_kit.yml
required_packages:
  - git
  - vim
  - tmux
  - jq
  - curl
  - wget
  - htop
  - nmap

required_files:
  - /etc/ssh/sshd_config
  - /etc/fstab
  - /var/log/syslog
```

### 3. Run the Auditor

Execute the playbook using `ansible-playbook`:

```bash
ansible-playbook -i inventory.ini survival_kit_auditor.yml
```

The playbook will output a summary for each host, indicating which items from your survival kit are missing.

## Automated Tests

To run the self-contained, offline tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_survival_kit_auditor.yml
```

These tests simulate different server states (all items present, some items missing) using mocked Ansible facts to ensure the playbook correctly identifies and reports the status without actual system interaction.
