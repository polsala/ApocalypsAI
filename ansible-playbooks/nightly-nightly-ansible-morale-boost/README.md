# Nightly Ansible Morale Booster

This Ansible playbook deploys a whimsical static webpage with morale-boosting content to target web servers. In the grim darkness of the post-apocalyptic future, a little cheer goes a long way! This utility ensures your community nodes always have a fresh dose of optimism, even if it's just a silly quote or a hopeful message.

## Features

*   **Static Content Deployment**: Easily pushes a templated HTML page to specified web server directories.
*   **Nginx Integration**: Configures Nginx to serve the morale-boosting page.
*   **Customizable Messages**: Update `vars/morale_content.yml` to change the quotes and messages.
*   **Idempotent**: Runs safely multiple times without unintended side effects.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers with appropriate permissions (e.g., `sudo` access for Nginx configuration).
*   Target servers should have Nginx installed or be able to install it via `apt` (Debian/Ubuntu) or `yum` (RHEL/CentOS).

### 1. Inventory Setup

Create an `inventory.ini` file (or use the provided `src/inventory.ini` as a template) listing your target servers.

```ini
[webservers]
server1.example.com
server2.example.com
```

### 2. Customize Morale Content (Optional)

Edit `src/vars/morale_content.yml` to define your desired quotes and messages.

```yaml
# src/vars/morale_content.yml
morale_quote: "Even in the darkest void, a tiny spark of hope can ignite a galaxy of smiles."
whimsical_message: "Remember, the best way to survive the apocalypse is with a good sense of humor and a well-stocked snack drawer!"
```

### 3. Run the Playbook

Execute the playbook from your control machine:

```bash
ansible-playbook -i src/inventory.ini src/deploy_morale.yml
```

This will:
1.  Ensure Nginx is installed.
2.  Create the `/var/www/morale_booster` directory.
3.  Render `src/templates/morale_page.html.j2` to `/var/www/morale_booster/index.html`.
4.  Configure Nginx to serve content from `/var/www/morale_booster` on port 80.
5.  Restart Nginx to apply changes.

After successful execution, you should be able to access the morale page by navigating to `http://<your_server_ip_or_hostname>` in a web browser.

## Testing

To run the self-contained tests for this utility, use the following command:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_deploy_morale.yml
```

This test playbook will simulate the deployment on `localhost` by creating the expected files and directories, and then assert their existence and content. It does not require Nginx to be actually installed or running on the machine executing the tests.
