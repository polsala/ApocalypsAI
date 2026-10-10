# Nightly Temporal Drift Corrector

## Overview
In the chaotic aftermath, temporal consistency is paramount. The `nightly-temporal-drift-corrector` is an Ansible playbook designed to synchronize system clocks across your fleet of servers, ensuring that all your machines operate on the same, correct timeline. This utility helps prevent issues caused by clock drift, which can impact logging, data integrity, and inter-service communication.

## Features
*   Installs and configures `ntp` or `chrony` (depending on distribution).
*   Ensures the NTP service is running and enabled.
*   Provides an option to force an immediate clock synchronization.

## Usage

### Prerequisites
*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions (e.g., `sudo` access).

### Inventory
Create an `inventory.ini` file in the `src/` directory listing your target hosts:

```ini
[drift_prone_servers]
server1.example.com
server2.example.com
```

### Variables
You can customize the NTP servers by creating a `vars/main.yml` file (e.g., in `src/vars/main.yml`) or passing variables via the command line.

```yaml
# src/vars/main.yml (optional)
ntp_servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org
force_sync: false # Set to true to force an immediate clock sync
```

### Running the Playbook
Execute the playbook using the `ansible-playbook` command from the utility's root directory:

```bash
ansible-playbook -i src/inventory.ini src/sync_clocks.yml -e "ansible_python_interpreter=/usr/bin/python3"
```

To force an immediate sync:
```bash
ansible-playbook -i src/inventory.ini src/sync_clocks.yml -e "force_sync=true ansible_python_interpreter=/usr/bin/python3"
```

## Testing

Tests are implemented as an Ansible playbook that runs against `localhost` in `check_mode`. This allows for verification of the playbook's syntax, variable resolution, conditional logic, and template rendering without making actual system changes or requiring remote hosts.

To run the tests:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_sync_clocks.yml -e "ansible_python_interpreter=/usr/bin/python3"
```
