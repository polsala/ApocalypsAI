# nightly-ansible-cert-checker

Verify SSL/TLS certificates on remote hosts using this Ansible playbook.

## Features

- Checks certificate expiration dates
- Validates certificate chains
- Reports misconfigured or soon-to-expire certs
- Supports custom ports and SNI

## Requirements

- Ansible 2.9+
- `openssl` installed on target hosts

## Usage

1. Update your inventory in `inventory.ini`
2. Run the playbook:

```bash
ansible-playbook -i inventory.ini cert_checker.yml
```

## Output

Generates a report at `reports/cert_report_*.txt` with findings.

## Testing

Run included tests with Molecule:

```bash
molecule test
```
