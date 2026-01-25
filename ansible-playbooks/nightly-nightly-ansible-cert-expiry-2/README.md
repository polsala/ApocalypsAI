# nightly-ansible-cert-expiry

Scan SSL/TLS certificates on remote hosts and report upcoming expirations.

## Overview

This Ansible playbook connects to remote hosts, retrieves SSL/TLS certificates from specified ports (default: 443), and checks their expiration dates. It generates a report of certificates that are nearing expiration (default: within 30 days).

## Requirements

- Ansible 2.9+
- `openssl` installed on the control node

## Usage

1. Define your inventory in `inventory.ini`.
2. Run the playbook:

```bash
ansible-playbook cert_expiry_scan.yml
```

### Optional Variables

- `cert_scan_ports`: List of ports to scan (default: `[443]`)
- `cert_expiry_warning_days`: Days before expiry to warn (default: `30`)

Example with custom ports:

```bash
ansible-playbook cert_expiry_scan.yml -e "cert_scan_ports=[443, 8443]"
```

## Output

Generates `cert_expiry_report.json` with expiry details.
