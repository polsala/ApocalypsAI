# Nightly Broadcast Beacon Manager

## Summary
This Ansible playbook deploys and manages a simple HTTP server (e.g., Nginx) on remote hosts, broadcasting critical community messages or 'beacon signals' to a network of survival outposts. It ensures a consistent communication channel is operational and can be updated centrally.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access to your target beacon hosts with `sudo` privileges.
- Python installed on target hosts (Ansible's default requirement).

### Files
- `src/deploy_beacon.yml`: The main playbook to deploy the beacon.
- `src/inventory.ini`: An example inventory file for your beacon hosts.
- `src/vars/main.yml`: Variables to customize the web server and beacon message content.
- `src/templates/beacon_message.html.j2`: The Jinja2 template for the HTML beacon message.
- `tests/test_deploy_beacon.yml`: A local test playbook to verify the template rendering and variable definitions.

### Running the Playbook
1.  **Customize `src/inventory.ini`**:
    Update `beacon_host_1`, `beacon_host_2`, `ansible_user`, and `ansible_ssh_private_key_file` (or `ansible_password`) to match your environment.

    ```ini
    [beacons]
    beacon_host_1 ansible_host=192.168.1.10
    beacon_host_2 ansible_host=192.168.1.11

    [all:vars]
    ansible_user=your_ssh_user
    # ansible_ssh_private_key_file=~/.ssh/id_rsa
    # ansible_become_password=your_sudo_password
    ```

2.  **Customize `src/vars/main.yml`**:
    Adjust `beacon_webserver_package`, `beacon_webserver_service`, `beacon_webserver_port`, `beacon_web_root`, and the `beacon_message_title`/`beacon_message_content` to your needs.

3.  **Run the deployment playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/deploy_beacon.yml
    ```

    To perform a dry run without making changes:
    ```bash
    ansible-playbook -i src/inventory.ini src/deploy_beacon.yml --check --diff
    ```

After successful deployment, you should be able to access the beacon message by navigating to `http://<beacon_host_ip>:<beacon_webserver_port>/index.html` in a web browser.

## Customization

- **Web Server**: By default, Nginx is used. You can change `beacon_webserver_package` and `beacon_webserver_service` in `src/vars/main.yml` to `apache2` for Apache, for example.
- **Message Content**: Modify `beacon_message_title` and `beacon_message_content` in `src/vars/main.yml` to update the broadcast message.
- **HTML Template**: For advanced styling or content, edit `src/templates/beacon_message.html.j2` directly.

## Testing

The `tests/test_deploy_beacon.yml` playbook provides an offline, deterministic way to verify the playbook's logic, variable definitions, and template rendering without deploying to actual remote hosts.

To run the tests:

```bash
ansible-playbook tests/test_deploy_beacon.yml
```

This test playbook will:
1.  Create a temporary directory on your local machine.
2.  Render the `beacon_message.html.j2` template into a file within that temporary directory, using the variables defined in `src/vars/main.yml` and local facts.
3.  Verify that the rendered file exists and contains the expected title and content.
4.  Assert that all required variables for the main playbook are defined.
5.  Clean up the temporary directory.
