# nightly-ansible-uptime-report

**Purpose**: Gather the human‑readable uptime (`uptime -p`) from each host in the inventory and render a concise report file (`uptime_report.txt`).

## How it works
1. The playbook runs the `uptime -p` command on every host.
2. The output is captured in the `uptime_result` variable.
3. A Jinja2 template turns the data into a friendly text report.

## Files
- `src/uptime_report.yml` – Main playbook.
- `src/inventory.ini` – Simple inventory (defaults to `localhost`).
- `src/templates/uptime_report.j2` – Jinja2 template for the report.
- `tests/test_uptime_report.yml` – Minimal test that validates the playbook syntax in check mode.

## Usage
```bash
ansible-playbook -i src/inventory.ini src/uptime_report.yml
```

Run with `--check` to perform a dry‑run (useful for CI):
```bash
ansible-playbook -i src/inventory.ini src/uptime_report.yml --check
```

The generated `uptime_report.txt` will be placed in the repository root.
