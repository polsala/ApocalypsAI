# Nightly Digital Bunker Fortifier

## Summary
This Ansible playbook fortifies your digital bunker (server) by ensuring essential security updates are applied, basic security tools are installed, and a custom 'survival message' is displayed upon login.

## Features
- Updates `apt` package cache and upgrades all installed packages.
- Installs `fail2ban` and `ufw` for basic intrusion prevention and firewall management.
- Configures `ufw` to enable the firewall, deny incoming connections by default, and allow SSH.
- Ensures `unattended-upgrades` is installed and configured for automatic security updates.
- Sets a whimsical 'Digital Bunker' Message Of The Day (MOTD).

## Requirements
- Ansible (version 2.10 or higher recommended)
- Target hosts must be running a Debian-based operating system (e.g., Ubuntu, Debian).
- `python3-apt` package on target hosts for `apt` module functionality.

## Usage
1.  **Prepare your inventory**: Create or modify an `inventory.ini` file to list your target servers (your 'digital bunkers').
    ```ini
    [bunkers]
    your_bunker_ip_or_hostname
    # another_bunker_ip_or_hostname
    ```
    For local testing, you can use `localhost` with `ansible_connection=local`:
    ```ini
    [bunkers]
    localhost ansible_connection=local
    ```

2.  **Run the playbook**:
    ```bash
    ansible-playbook -i src/inventory.ini src/fortify_bunker.yml --ask-become-pass
    ```
    (The `--ask-become-pass` flag will prompt for the `sudo` password on your target hosts.)

3.  **Customize (Optional)**: You can override the `bunker_motd_message` or other variables by creating a `vars/main.yml` file or passing `--extra-vars`:
    ```bash
    ansible-playbook -i src/inventory.ini src/fortify_bunker.yml --extra-vars "bunker_motd_message='Stay safe, survivor!'" --ask-become-pass
    ```

## Testing
To run the automated tests, execute the `run_tests.sh` script:

```bash
bash tests/run_tests.sh
```

This script performs a syntax check and a check-mode run with mocked variables to ensure the playbook is well-formed and would attempt to make the expected changes without modifying your system.
