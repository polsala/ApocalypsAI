# nightly-ansible-cert-expiry-6

A robust Ansible playbook to scan remote hosts for TLS certificate expiration dates and generate actionable HTML reports.

## Features

- Scans specified hosts for certificate files
- Detects certificates nearing expiration (configurable threshold)
- Generates human-readable HTML report
- Idempotent and safe to run in production environments

## Requirements

- Ansible 2.9+
- OpenSSL installed on target hosts

## Usage

```bash
ansible-playbook -i inventory.ini cert_expiry_scan.yml
```

### Custom Threshold

Set custom warning days via `cert_warning_days` variable:

```bash
ansible-playbook -i inventory.ini cert_expiry_scan.yml -e cert_warning_days=60
```

## Inventory Format

Example `inventory.ini`:

```
[webservers]
web1.example.com
web2.example.com
```

## Output

Generates `cert_report.html` in the playbook directory with full details.
