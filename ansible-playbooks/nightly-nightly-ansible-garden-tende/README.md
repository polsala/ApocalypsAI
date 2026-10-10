# Nightly Ansible Garden Tender

## Summary
This Ansible playbook, `nightly-ansible-garden-tender`, is designed to whimsically automate the setup and basic maintenance of virtual 'survival garden' plots on remote servers. It ensures that essential tools are installed, creates dedicated 'gardener' user accounts, sets up designated plot directories, and simulates routine care tasks like 'watering' and 'harvesting'. It's a fun way to manage distributed virtual resources with an apocalyptic twist.

## Features
- Installs essential system tools (`jq`, `curl`, `git`) for future 'garden management' scripts.
- Creates a dedicated system user and group for each 'gardener'.
- Establishes a base directory for all survival gardens (`/opt/survival_garden`).
- Creates specific plot directories (e.g., `/opt/survival_garden/plot_alpha`) with appropriate ownership and permissions.
- Simulates daily 'watering' by touching a `watered_today.log` file.
- Simulates 'harvesting' by creating a timestamped `harvest_report_YYYYMMDDTHHMMSS.log` file.
- Provides a debug report on the status of each tended garden.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access to your target servers (if not running locally).
- Python interpreter on target servers.

### 1. Inventory Setup
Create an `inventory.ini` file (or modify the provided example) to define your target servers. For local testing, `localhost` can be used.

```ini
[garden_servers]
localhost ansible_connection=local
# server1.example.com
# server2.example.com

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### 2. Run the Playbook
Execute the playbook using the `ansible-playbook` command. You can specify variables directly or let the defaults apply.

```bash
ansible-playbook -i inventory.ini playbook.yml
```

#### Example with custom variables:
To tend to a specific plot with a custom gardener:

```bash
ansible-playbook -i inventory.ini playbook.yml \
  -e 'garden_plot_name="oasis_plot"' \
  -e 'garden_owner_username="oasis_keeper"' \
  -e 'garden_owner_uid=2000' \
  -e 'garden_owner_gid=2000'
```

### 3. Explore the Garden
After running, you can SSH into your target server(s) and check the `/opt/survival_garden` directory:

```bash
ssh user@server1.example.com
ls -l /opt/survival_garden/plot_alpha/
cat /opt/survival_garden/plot_alpha/watered_today.log
```

## Configuration Variables
The `roles/garden_plot/defaults/main.yml` file defines default variables. You can override these in your inventory, command line (`-e`), or by creating a `vars/main.yml` file.

- `garden_plot_name`: (Default: `default_plot`) The name of the specific garden plot to manage.
- `garden_owner_username`: (Default: `survival_gardener`) The username for the dedicated gardener account.
- `garden_owner_uid`: (Default: `1000`) The UID for the gardener user. Ensure it's unique if specifying.
- `garden_owner_gid`: (Default: `1000`) The GID for the gardener group. Ensure it's unique if specifying.
- `garden_base_path`: (Default: `/opt/survival_garden`) The base directory where all garden plots will reside.

## Testing

To run the automated tests for this playbook, execute the following command:

```bash
ansible-playbook -i inventory.ini tests/test_playbook.yml --syntax-check
ansible-playbook -i inventory.ini tests/test_playbook.yml --diff
```
The `test_playbook.yml` runs the main role against `localhost` with mocked facts and asserts expected outcomes, including idempotence for setup tasks and expected changes for whimsical tasks. It also includes cleanup of test directories.
