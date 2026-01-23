# nightly-ansible-cert-expiry-scan

Scan remote hosts for SSL/TLS certificate expiration using Ansible.

## Overview

This utility runs an Ansible playbook to check the expiration dates of SSL/TLS certificates on target hosts. It helps identify certificates nearing expiry and reports them in a structured format.

## Requirements

- Ansible 2.9+
- `openssl` installed on target hosts

## Usage

1. Update `inventory.ini` with your target hosts.
2. Run the playbook:

```bash
ansible-playbook cert_expiry_scan.yml
```

## Output

The playbook outputs a report listing each host, port, and certificate expiration date. Certificates expiring within 30 days are highlighted.

## Testing

Run the test suite with Molecule:

```bash
molecule test
```
