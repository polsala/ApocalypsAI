# Plant Watering Scheduler

A whimsical Ansible playbook that pretends to schedule watering of your indoor plants by toggling a smart plug. Perfect for eco‑friendly role‑playing in a post‑apocalyptic garden.

## Usage

```bash
ansible-playbook -i inventory src/water_plants.yml
```

The playbook sets a fact `watering_scheduled` to `true`. You can extend it to call your Home Assistant API.

## Files

- `src/water_plants.yml` – main playbook
- `tests/test_water_plants.yml` – simple test that asserts the fact is set
