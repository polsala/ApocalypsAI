# Nightly Plant Watering Scheduler

A whimsical Ansible playbook that sets up a daily cron job to water your houseplants using a smart plug. The playbook installs `curl` if needed and creates a cron entry that sends an HTTP request to toggle the plug at a configurable time.

## Usage

```bash
ansible-playbook -i src/inventory.ini src/water_plants.yml
```

## Variables

- `watering_time`: Time of day in HH:MM (24h) when watering should occur (default: "08:00").
- `plug_endpoint`: URL to trigger the smart plug (default: "http://localhost:8080/toggle").

## Files

- `src/water_plants.yml` – Main playbook.
- `src/inventory.ini` – Inventory (localhost).
- `tests/test_water_plants.yml` – Simple test that ensures the cron job is created.
