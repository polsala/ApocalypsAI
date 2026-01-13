# nightly-uptime-report

**Purpose**: Collect the system uptime from a list of hosts and produce a humanâreadable report (`uptime_report.txt`). This utility is useful for quick health checks of a fleet of machines without writing custom scripts.

## Files

- `src/uptime_report.yml` â The main Ansible playbook.
- `src/inventory.ini` â Sample inventory defining target hosts (default uses localhost).
- `src/templates/uptime_report.j2` â Jinja2 template for the final report.
- `tests/test_uptime_report.py` â Automated test that runs the playbook locally and verifies the output.

## How to run

```bash
# Install Ansible if not already present
python -m pip install ansible

# Execute the playbook (uses the provided inventory)
ansible-playbook -i src/inventory.ini src/uptime_report.yml

# After a successful run, you will find `uptime_report.txt` in the current directory.
cat uptime_report.txt
```

The playbook is written to be idempotent and safe to run multiple times. It works with any inventory â just point `-i` to your own hosts file.

## Testing

Run the test suite with pytest (the repository already includes pytest as a dev dependency):

```bash
python -m pip install pytest
pytest tests/test_uptime_report.py
```

The test uses a local inventory and a harmless `echo` command to simulate uptime, ensuring deterministic, offline execution.

