# nightly-ansible-config-drift-detector

## Overview

`nightly-ansible-config-drift-detector` is a tiny, self‑contained Ansible playbook that helps you detect configuration drift. It compares a *baseline* configuration (the expected state) with a *current* configuration snapshot and sets a boolean variable `drifted` indicating whether the two differ.

## Why?

In many DevOps workflows you keep a reference configuration file (e.g., a `.env` template, a `nginx.conf` baseline, etc.). Over time the live system may diverge due to manual edits or failed deployments. This playbook gives you a quick, reproducible way to spot that drift without writing custom scripts.

## Files

- `src/detect_drift.yml` – The core playbook.
- `tests/test_no_drift.yml` – Unit‑style test where baseline and current match (expects `drifted == false`).
- `tests/test_with_drift.yml` – Test where they differ (expects `drifted == true`).

## Usage

```bash
# Run a no‑drift test (should pass)
ansible-playbook tests/test_no_drift.yml

# Run a drift test (should pass)
ansible-playbook tests/test_with_drift.yml
```

You can also invoke the core playbook directly by providing the two variables:

```bash
ansible-playbook src/detect_drift.yml \
  -e "baseline_content='foo=bar'" \
  -e "current_content='foo=baz'"
```

The playbook will output a debug message like `Drift detected: true` and expose the variable `drifted` for downstream tasks.

## License

MIT – feel free to copy, modify, and share.
