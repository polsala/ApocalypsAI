# Nightly Ansible Morale Beacon

## Summary
An Ansible playbook to deploy and maintain a "Morale Beacon" service, ensuring a critical message broadcast system is always operational and updated with whimsical, morale-boosting content for the ApocalypsAI community.

## Purpose
In the ever-shifting landscape of the apocalypse, morale is a critical resource. The Morale Beacon ensures a consistent, whimsical stream of encouragement is broadcast, keeping spirits high and circuits humming. This utility deploys a simple Flask web application that serves a random morale-boosting message, ensuring the beacon is always active and ready to uplift.

## Usage

### Prerequisites
- Ansible installed on your control machine.
- Python 3 and `pip` on the target host(s).
- SSH access to the target host(s) with appropriate permissions (e.g., `sudo` access).

### Files
- `src/playbook.yml`: The main Ansible playbook to deploy the Morale Beacon.
- `src/inventory.ini`: An example inventory file.
- `src/app.py`: The Python Flask application that serves morale messages.
- `src/morale_messages.txt`: A list of pre-defined morale messages.
- `src/templates/morale_beacon.service.j2`: Jinja2 template for the systemd service file.
- `tests/test_playbook.yml`: Playbook for testing the deployment logic.

### How to Run

1.  **Define your target hosts**: Edit `src/inventory.ini` to include the IP addresses or hostnames of your target servers.
    ```ini
    [morale_beacons]
    your_server_ip_1
    your_server_ip_2
    ```

2.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml --ask-become-pass
    ```
    (You might need `--ask-pass` if not using SSH keys, or `--private-key` if using a specific key).

3.  **Verify deployment**: Once the playbook completes, you should be able to access the Morale Beacon on port `5000` (default) of your target server:
    ```bash
    curl http://your_server_ip_1:5000/
    ```
    This should return a whimsical morale message.

## Configuration
- **`app_port`**: The port the Flask application will listen on. Default is `5000`. Can be overridden in `src/inventory.ini` or as an extra var:
    ```bash
    ansible-playbook -i src/inventory.ini src/playbook.yml -e "app_port=8080"
    ```
- **`app_dir`**: The directory where the Flask application files will be deployed. Default is `/opt/morale_beacon`.

## Testing
To run the offline, deterministic tests:
```bash
ansible-playbook -i tests/test_inventory.ini tests/test_playbook.yml
```
These tests simulate the state of a target host after the playbook has run and assert that the expected components (packages, files, service status) would be in place.
