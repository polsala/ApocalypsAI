# nightly-ansible-cert-expiry-6

A robust Ansible playbook to scan remote hosts for expiring TLS certificates and generate an HTML report.

## Features

- Scans remote hosts for TLS certificate expiration
- Generates a human-readable HTML report
- Configurable warning thresholds
- Idempotent and safe to run

## Requirements

- Ansible 2.9+
- `sslv` module (bundled)

## Usage

1. Define your inventory in `inventory.ini`
2. Run the playbook:

```bash
ansible-playbook cert_expiry_scan.yml
```

## Configuration

Edit `vars/config.yml` to adjust thresholds and scan settings.

## Output

The playbook generates `cert_report.html` in the playbook root after execution.
