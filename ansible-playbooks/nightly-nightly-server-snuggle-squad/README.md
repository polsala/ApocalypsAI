# Nightly Server Snuggle Squad

## Summary

The `nightly-server-snuggle-squad` is an Ansible playbook designed to bring a touch of whimsy and ensure basic 'comfort' and 'hygiene' across your server fleet. It establishes a dedicated 'comfort zone' directory, logs daily 'bedtime stories' (whimsical, timestamped messages), and sets up a 'dream catcher' cron job for light maintenance or logging.

## Features

*   **Comfort Blanket**: Creates a `/opt/server_comfort` directory to serve as a designated 'comfort zone' for your servers.
*   **Bedtime Story**: Appends a unique, timestamped, and whimsical message to `/opt/server_comfort/bedtime_log.txt` each time the playbook runs, offering a 'good night' or 'dreaming' message.
*   **Dream Catcher**: Deploys a simple shell script (`dream_catcher.sh`) and schedules it via cron to run daily at 3 AM. This script can be extended for actual light maintenance (e.g., temporary file cleanup) or simply to log another whimsical 'dream processing' message.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access to your target servers (or `ansible_connection=local` for localhost).
    *   `sudo` privileges on target servers for creating directories and cron jobs.

2.  **Inventory**: Update the `inventory.ini` file with your target servers. For testing on localhost, the provided `inventory.ini` is sufficient.

    ```ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

3.  **Run the Playbook**:

    ```bash
    ansible-playbook -i inventory.ini snuggle_squad.yml
    ```

    To run against specific hosts:

    ```bash
    ansible-playbook -i inventory.ini snuggle_squad.yml --limit server1.example.com
    ```

4.  **Verify (on target server)**:

    ```bash
    ls -l /opt/server_comfort/
    cat /opt/server_comfort/bedtime_log.txt
    cat /opt/server_comfort/dream_catcher.sh
    sudo crontab -l -u root | grep server_dream_catcher
    ```

## Development & Testing

To run the automated tests, ensure you have Ansible installed and then execute:

```bash
ansible-playbook -i inventory.ini tests/test_snuggle_squad.yml
```

This will run the playbook against `localhost`, verify its effects, and clean up afterwards. The tests are designed to be deterministic and offline.
