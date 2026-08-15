# Plant Watering Scheduler

This Ansible playbook sets up a daily cron job that triggers a smart plug to water your plants. It is whimsical yet practical for home automation enthusiasts.

## Requirements

- Ansible 2.9+
- Access to the smart plug's HTTP API (IP address)

## Variables

- `plant_watering_plug_ip` (string): IP address of the smart plug.
- `plant_watering_time` (string, default "07:00"): Time of day to water plants (24h format).

## Usage

```bash
ansible-playbook -i inventory.ini src/playbook.yml -e "plant_watering_plug_ip=192.168.1.50 plant_watering_time=07:00"
```

The playbook will create a cron job that runs a `curl` command to toggle the plug at the specified time.
