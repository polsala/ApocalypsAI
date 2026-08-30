# Nightly Temporal Sync Beacon

## Summary
This Ansible playbook, the "Temporal Sync Beacon," is designed to ensure precise time synchronization across your fleet of servers. It detects and corrects "temporal drift" by installing and configuring a Network Time Protocol (NTP) client (preferring `chrony` over `ntpd`) and ensuring the service is running and enabled. Maintaining accurate time is crucial for logging, security, distributed systems, and overall operational integrity in any post-apocalyptic or pre-apocalyptic environment.

## How it Works
1.  **Fact Gathering**: Gathers system facts to determine the operating system and available service managers.
2.  **NTP Client Installation**: Installs `chrony` if available and preferred, otherwise falls back to `ntpd`.
3.  **Configuration**: Configures the chosen NTP client with default NTP pool servers (`pool.ntp.org`).
4.  **Service Management**: Ensures the NTP service is started and enabled to run on boot.
5.  **Status Reporting**: Provides output on the NTP service status and current system time.

## Usage

### Prerequisites
*   Ansible installed on your control machine.
*   SSH access to your target servers with `sudo` privileges.
*   An `inventory.ini` file defining your target hosts.

### 1. Define Your Inventory
Create an `inventory.ini` file (or use an existing one) that lists your target servers. For example:

```ini
[servers]
server1.example.com
server2.example.com
```

### 2. Run the Playbook
Execute the playbook using the `ansible-playbook` command:

```bash
ansible-playbook -i src/inventory.ini src/temporal_sync.yml --ask-become-pass
```

Replace `src/inventory.ini` with the path to your inventory file. The `--ask-become-pass` flag will prompt for the sudo password on your target hosts.

### 3. Verify Synchronization
After running, you can manually verify the NTP status on a target server:

```bash
sudo chronyc tracking # If chrony is used
sudo ntpq -p        # If ntpd is used
date
```

## Testing

To run the self-contained, offline tests for this utility, use the following command:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_temporal_sync.yml
```

This will execute a test playbook against `localhost` that simulates different system states to verify the core logic of `temporal_sync.yml` without making actual changes or requiring network access.
