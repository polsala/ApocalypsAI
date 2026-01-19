# nightly-ansible-cert-checker

Verify SSL/TLS certificates on remote hosts using this Ansible playbook.

## Overview

This utility checks the expiration date and validity of SSL/TLS certificates on specified hosts. It supports both direct file paths and remote URLs. Results are reported in a clean, human-readable format.

## Requirements

- Ansible 2.9+
- `openssl` installed on target hosts

## Usage

1. Define your inventory in `inventory.ini`
2. Run the playbook:

```bash
ansible-playbook cert_checker.yml
```

## Configuration

Edit `inventory.ini` to specify target hosts and certificate locations.

## Output

A report is generated showing:
- Hostname
- Certificate subject
- Expiration date
- Days until expiration
- Validity status
