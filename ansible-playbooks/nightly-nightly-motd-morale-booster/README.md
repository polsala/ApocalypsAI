# Nightly MOTD Morale Booster

## Summary
This Ansible playbook deploys whimsical, morale-boosting Messages of the Day (MOTD) or survival tips to remote servers. It ensures consistent positive reinforcement and useful information is displayed to users upon login across your ApocalypsAI-managed infrastructure.

## How it Works
1.  **Message Selection**: The playbook selects a random message from a predefined list of morale-boosting quotes or survival tips (defined in `vars/motd_messages.yml`).
2.  **Templating**: It uses a Jinja2 template (`src/templates/motd.j2`) to format the selected message into a visually appealing MOTD.
3.  **Deployment**: The formatted MOTD is then deployed to `/etc/motd` on all target servers, replacing any existing content. This requires `become: true` (root privileges).
4.  **Idempotency**: The playbook is designed to be idempotent. Running it multiple times with the same message will not cause further changes.

## Requirements
*   Ansible (version 2.9 or higher recommended)
*   Access to target servers via SSH with appropriate permissions for `become` (sudo).

## Usage
1.  **Define your inventory**: Create or update an `inventory.ini` file with your target servers.
    ```ini
    [servers]
    server1.example.com
    server2.example.com
    # Add more servers here
    
    [all:vars]
    ansible_user=your_ssh_user
    ```
2.  **Customize Messages (Optional)**: Edit `vars/motd_messages.yml` to add, remove, or modify the morale-boosting messages.
3.  **Run the playbook**: Execute the playbook using the `ansible-playbook` command.
    ```bash
    ansible-playbook -i src/inventory.ini src/deploy_motd.yml --ask-become-pass
    ```
    (Replace `--ask-become-pass` with `--become-user <user>` or other privilege escalation methods as needed).

## Configuration
*   `src/inventory.ini`: Your Ansible inventory file specifying target hosts.
*   `src/deploy_motd.yml`: The main playbook logic.
*   `src/templates/motd.j2`: The Jinja2 template for the MOTD content. You can customize its layout.
*   `vars/motd_messages.yml`: A YAML file containing a list of strings, each representing a potential MOTD message. The playbook will randomly select one from this list.

## Testing
To ensure the playbook functions correctly and is idempotent, run the provided test playbook:

```bash
ansible-playbook -i src/inventory.ini tests/test_deploy_motd.yml --ask-become-pass
```

This test playbook will:
1.  Create a temporary environment.
2.  Run the main `deploy_motd.yml` playbook against `localhost` (redirecting output to a temporary file).
3.  Verify that the temporary MOTD file is created and contains the expected content.
4.  Run the main playbook again to confirm idempotency (no further changes reported).
5.  Clean up all temporary files.
