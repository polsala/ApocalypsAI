# Nightly Ansible Comfort File Distributor

## Summary
This Ansible playbook distributes a whimsical "comfort file" (a motivational ASCII art message) to all managed servers, ensuring a touch of digital warmth and verifying its presence and content. It's a lighthearted take on configuration compliance and baseline file management.

## Classifier
`ansible-playbooks`

## Usage

### Prerequisites
- Ansible installed (version 2.9 or higher recommended).
- SSH access to your target servers (if not running on localhost).
- Python on target servers (for Ansible modules).

### Files
- `src/distribute_comfort_file.yml`: The main playbook to distribute the comfort file.
- `src/inventory.ini`: An example inventory file. Modify it to include your target servers.
- `src/files/comfort_message.txt`: The actual comfort message content.
- `tests/test_distribute_comfort_file.yml`: A self-contained test playbook.

### How to Run

1.  **Prepare your inventory:**
    Edit `src/inventory.ini` to list the servers where you want to deploy the comfort file. For local testing, `localhost` is pre-configured.

    ```ini
    # src/inventory.ini
    [servers]
    localhost ansible_connection=local
    # server1.example.com
    # server2.example.com
    ```

2.  **Run the playbook:**
    Execute the playbook using `ansible-playbook`. You might need `sudo` privileges on the target server to write to `/etc/apocalypsai`.

    ```bash
    ansible-playbook -i src/inventory.ini src/distribute_comfort_file.yml --ask-become-pass
    ```
    (Remove `--ask-become-pass` if you have passwordless sudo configured or are not using `become: yes`).

    The playbook will:
    - Create the `/etc/apocalypsai` directory (if it doesn't exist).
    - Copy `comfort_message.txt` into it.
    - Verify the file's existence and content.

## Automated Tests

This utility includes a self-contained test playbook that runs against `localhost`. It simulates the deployment and verification process without requiring actual remote infrastructure.

### How to Run Tests

```bash
ansible-playbook -i src/inventory.ini tests/test_distribute_comfort_file.yml --ask-become-pass
```

The test playbook will:
1.  Clean up any previous test artifacts from `/tmp/apocalypsai_test_comfort_file`.
2.  Create a temporary directory `/tmp/apocalypsai_test_comfort_file`.
3.  "Deploy" a mock comfort file into this temporary directory.
4.  Verify the existence and content of the mock comfort file using `stat` and `slurp` modules.
5.  Clean up the temporary directory.

This ensures the logic for file distribution and content verification works as expected in a deterministic and isolated environment.
