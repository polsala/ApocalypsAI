## Nightly Ansible Config Sync

This utility automates the synchronization of Ansible inventory and playbook configurations across a set of remote hosts. It leverages Ansible Vault for secure handling of sensitive data.

### Purpose

In a post-apocalyptic world, maintaining consistent and secure configurations across distributed systems is paramount. This tool ensures that your Ansible control plane's state is mirrored across designated nodes, preventing configuration drift and enabling rapid deployment of critical updates.

### Features

*   **Secure Synchronization**: Uses Ansible Vault to encrypt and decrypt sensitive configuration files during transfer.
*   **Inventory Mirroring**: Replicates the `inventory.ini` file to target hosts.
*   **Playbook Replication**: Copies specified playbook directories to target hosts.
*   **Idempotent Operations**: Ansible's nature ensures that configurations are only applied if they differ.

### Prerequisites

*   Ansible installed on the control node.
*   SSH access to the target hosts.
*   Ansible Vault password file (or interactive password entry).

### Usage

1.  **Prepare your Ansible environment**: Ensure your `inventory.ini` and playbook directories are in the correct location on your control node.
2.  **Create a Vault password file**: For non-interactive use, create a file (e.g., `.vault_pass`) containing your Ansible Vault password.
3.  **Run the playbook**: Execute the main playbook, specifying the vault password file if used.

```bash
# Example using a vault password file
ansible-playbook sync_configs.yml --vault-password-file .vault_pass

# Example with interactive password entry
ansible-playbook sync_configs.yml
```

### Configuration

The `vars/main.yml` file allows you to customize the synchronization process:

*   `target_hosts`: A list of hostnames or IP addresses where configurations will be synchronized.
*   `inventory_source`: The path to the local `inventory.ini` file.
*   `playbook_sources`: A list of paths to local playbook directories to synchronize.
*   `destination_base_path`: The base directory on the remote hosts where configurations will be placed.

### Testing

Automated tests are included to verify the functionality of the playbook without requiring actual remote hosts. These tests mock Ansible's execution and check the generated tasks.

```bash
# Run tests (requires ansible-galaxy collection install ansible-core --collections-dir ./tests/ansible_collections)
ansible-playbook tests/test_sync_configs.yml
```
