# Nightly Perimeter Shield Fortifier

## Summary

In the digital wasteland, your servers are fortresses. This Ansible playbook, the "Perimeter Shield Fortifier," ensures your digital defenses are up by configuring basic firewall rules. It intelligently detects your operating system (Debian/Ubuntu for UFW, RedHat/CentOS for firewalld) and sets up essential access points while denying the rest, protecting your critical infrastructure from unseen threats.

## Features

*   **OS-Aware Firewalling**: Automatically uses UFW for Debian/Ubuntu-based systems and firewalld for RedHat/CentOS-based systems.
*   **Essential Port Configuration**: Configures rules to allow SSH (port 22) and common web traffic (HTTP/HTTPS on ports 80, 443) by default.
*   **Customizable Access**: Easily adjust allowed ports and firewall policies via variables.
*   **Idempotent**: Running the playbook multiple times will result in the same desired state without unnecessary changes.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target servers with appropriate permissions (e.g., `sudo` access).

2.  **Inventory**:
    Create an `inventory.ini` file (or use an existing one) listing your target servers. For example:

    ```ini
    [wasteland_servers]
    server1.example.com
    server2.example.com
    ```

3.  **Variables**:
    Review and optionally customize the `vars/main.yml` file. You can override these variables directly in your inventory or via `ansible-playbook` command-line arguments.

    ```yaml
    # vars/main.yml
    ---
    allowed_tcp_ports:
      - 22 # SSH
      - 80 # HTTP
      - 443 # HTTPS

    # Set to 'ufw' or 'firewalld' to force a specific firewall,
    # or leave empty for auto-detection.
    force_firewall_type: ""

    # Default policy for incoming connections (e.g., 'deny', 'allow')
    default_incoming_policy: "deny"
    ```

4.  **Run the Playbook**:
    Execute the playbook using the `ansible-playbook` command:

    ```bash
    ansible-playbook -i inventory.ini src/fortify_perimeter.yml --ask-become-pass
    ```

    *   `--ask-become-pass`: Prompts for the `sudo` password on target hosts.
    *   `-i inventory.ini`: Specifies your inventory file.

5.  **Check Mode (Dry Run)**:
    To see what changes the playbook would make without actually applying them, use `--check`:

    ```bash
    ansible-playbook -i inventory.ini src/fortify_perimeter.yml --check --ask-become-pass
    ```

## Testing

The `tests/test_fortify_perimeter.yml` playbook provides a deterministic, offline way to verify the playbook's logic. It uses `set_fact` to mock `ansible_facts` and `assert` to check if the correct firewall type is identified and if the tasks for that firewall would be executed.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_fortify_perimeter.yml
```

This will simulate different OS environments and verify the playbook's conditional logic without requiring actual server access or firewall modifications.
