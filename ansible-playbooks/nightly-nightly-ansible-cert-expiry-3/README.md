# nightly-ansible-cert-expiry-3

A robust Ansible playbook to scan remote hosts for SSL/TLS certificate expiration dates and generate an HTML report.

## Features

- Scans HTTPS endpoints for certificate expiry
- Generates a detailed HTML report with color-coded warnings
- Supports custom ports and multiple hosts
- Includes unit tests with mock data

## Requirements

- Ansible 2.9+
- `openssl` installed on target hosts

## Usage

```bash
ansible-playbook cert_expiry_scan.yml -i inventory.ini
```

## Inventory Example

```ini
[webservers]
web1.example.com
web2.example.com:8443
```

## Output

The playbook generates `cert_report.html` in the current directory.
