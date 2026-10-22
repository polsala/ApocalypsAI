# Nightly Safehouse Setup

## Overview

`nightly-safehouse-setup` is a tiny Ansible playbook that creates a mock "safehouse" directory under `/tmp/safehouse`.  It populates three essential sub‑folders – **food**, **water**, and **tools** – each with a placeholder file.  The playbook is completely self‑contained, runs against the local host, and requires only Ansible (no external services).

## Files

- `src/setup_safehouse.yml` – The main playbook that creates the directory tree.
- `inventory.ini` – Simple inventory pointing to `localhost`.
- `tests/test_safehouse.yml` – An integration test that runs the playbook and asserts the expected files exist, then cleans up.

## Usage

```bash
# Install Ansible if you don't have it
python3 -m pip install ansible

# Run the playbook
ansible-playbook -i inventory.ini src/setup_safehouse.yml
```

The safehouse will appear at `/tmp/safehouse`.  To verify it was created correctly, run the test playbook:

```bash
ansible-playbook -i inventory.ini tests/test_safehouse.yml
```

The test will execute the setup, check that all directories and placeholder files exist, and finally remove the `/tmp/safehouse` directory so the test is repeatable.

## License

MIT – feel free to adapt, remix, and deploy in your own post‑apocalyptic simulations!
