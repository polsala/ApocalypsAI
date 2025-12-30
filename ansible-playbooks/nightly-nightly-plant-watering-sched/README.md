# Plant Watering Scheduler

This Ansible playbook configures a Raspberry Pi (or any Linux host) to water houseplants automatically. It installs the required pump control script, creates a systemd service, and schedules a daily cron job at a configurable time.

## Features

- Installs a simple Bash script that toggles a GPIO pin to activate a water pump.
- Creates a systemd service to manage the script.
- Sets up a cron job (via systemd timer) to run the service every day at the desired hour.
- All configuration is driven by variables in `vars/main.yml`.

## Requirements

- Ansible 2.9+
- Target host with `gpio` command available (e.g., Raspberry Pi OS)
- SSH access to the target host

## Usage

```bash
ansible-playbook -i inventory.ini playbook.yml
```

Edit `vars/main.yml` to adjust the watering time and GPIO pin.

## License

MIT
