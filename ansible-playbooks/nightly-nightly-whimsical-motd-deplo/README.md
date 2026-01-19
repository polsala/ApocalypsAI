# Nightly Whimsical MOTD Deployer

## Summary

This Ansible playbook deploys a randomly selected whimsical "Message of the Day" (MOTD) to target servers. It's designed to inject a bit of humor and personality into your system login screens, reminding users that even in the apocalypse, a good laugh (or a strange thought) can brighten the day.

## Features

*   **Random Selection**: Picks a different whimsical message from a predefined list for each deployment.
*   **Idempotent**: Ensures the MOTD file is updated only when the message changes.
*   **Configurable Messages**: Easily add or modify the list of whimsical messages.
*   **Permissions Management**: Sets appropriate permissions for the `/etc/motd` file.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers with `sudo` privileges.

### 1. Inventory Setup

Create an `inventory.ini` file (or use an existing one) that lists your target servers. For local testing, you can use `localhost`:

```ini
[servers]
localhost ansible_connection=local
# other_server_1 ansible_host=192.168.1.10
# other_server_2 ansible_host=your.remote.host
```

### 2. Customize Messages (Optional)

The default whimsical messages are located in `vars/motd_messages.yml`. You can edit this file to add, remove, or modify messages:

```yaml
motd_messages:
  - "Beware of rogue squirrels. They hoard nuts and bandwidth."
  - "Your system is 99% water and 1% pure digital magic."
  - "Remember to hydrate your servers. They get thirsty too!"
  - "The void stares back, but at least it's well-configured."
  - "Today's forecast: 100% chance of efficient operations."
  - "Don't panic. The answer is 42, or maybe just a reboot."
```

### 3. Run the Playbook

Execute the playbook using the `ansible-playbook` command, specifying your inventory file:

```bash
ansible-playbook -i inventory.ini motd_deployer.yml
```

This will connect to the servers listed in your `inventory.ini` and update their `/etc/motd` file with a new, randomly selected whimsical message.

## Testing

To ensure the playbook works as expected without modifying your actual `/etc/motd` file, a dedicated test playbook is provided. This test runs locally, writes to a temporary file, and verifies its content.

### 1. Test Inventory Setup

Ensure `tests/inventory_test.ini` is configured for local execution:

```ini
[test_servers]
localhost ansible_connection=local
```

### 2. Run Tests

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_motd_deployer.yml
```

The test playbook will:

1.  Define a temporary MOTD path (e.g., `/tmp/test_motd_ansible_<timestamp>`).
2.  Include and run the `motd_deployer.yml` playbook, overriding the `motd_path` variable.
3.  Read the content of the temporary file.
4.  Assert that the content matches one of the expected whimsical messages.
5.  Clean up the temporary file and its parent directory.

This provides a deterministic and offline test of the playbook's core logic.
