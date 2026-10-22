# Nightly Ansible MOTD Morale

This Ansible playbook, `nightly-ansible-motd-morale`, is designed to inject a dose of whimsy and morale into your server infrastructure. In the bleak post-apocalyptic landscape, a little cheer can go a long way. This utility deploys a randomly selected, pre-defined, morale-boosting message as the Message of the Day (MOTD) on your target servers.

## Features

*   **Whimsical Messages**: Choose from a curated list of uplifting and humorous messages.
*   **Random Selection**: A different message can greet users on each deployment.
*   **Idempotent**: Ensures the MOTD is set without unnecessary changes.
*   **Customizable**: Easily add or modify the list of messages.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions (e.g., `sudo` access for writing to `/etc/motd`).

### Files

*   `src/motd_deploy.yml`: The main Ansible playbook.
*   `src/inventory.ini`: An example inventory file. Customize this with your target hosts.
*   `src/templates/motd_template.j2`: The Jinja2 template for the MOTD file. It uses `ansible_hostname` and `ansible_date_time` facts.
*   `src/vars/motd_messages.yml`: A YAML file containing the list of morale-boosting messages.

### Running the Playbook

1.  **Customize your inventory**: Edit `src/inventory.ini` to list your target servers.

    ```ini
    [webservers]
    web1.example.com
    web2.example.com

    [databases]
    db1.example.com

    [all:vars]
    ansible_user=your_ssh_user
    ansible_become=true
    ```

2.  **(Optional) Customize messages**: Edit `src/vars/motd_messages.yml` to add or modify the messages.

    ```yaml
    # src/vars/motd_messages.yml
    motd_messages:
      - "May your code compile on the first try!"
      - "Remember, even a broken clock is right twice a day. You're better than a broken clock!"
      - "Your efforts are the keystones of our digital fortress. Keep building!"
      - "The coffee machine is working. That's a win!"
    ```

3.  **Run the playbook**: Execute the playbook from the `nightly-ansible-motd-morale` directory.

    ```bash
    ansible-playbook -i src/inventory.ini src/motd_deploy.yml
    ```

    This will connect to your servers, select a random message, and update their `/etc/motd` file.

## Testing

This utility includes a self-contained test playbook to verify its functionality without requiring actual remote servers or modifying your system's `/etc/motd`.

### Running Tests

1.  Ensure Ansible is installed.
2.  Execute the test playbook:

    ```bash
    ansible-playbook -i tests/inventory_test.ini tests/test_motd_deploy.yml
    ```

    The test playbook will:
    *   Create a temporary file on `localhost`.
    *   Run the `motd_deploy.yml` playbook, directing it to write to the temporary file and using a specific test message.
    *   Verify that the temporary file contains the expected MOTD content.
    *   Clean up the temporary file.

    A successful test run will show `changed=1` for the MOTD deployment and `ok=...` for assertions and cleanup, with no failures.
