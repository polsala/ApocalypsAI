# nightly-ssh-key-audit

Utility to audit SSH private keys in a directory. Checks file permissions (must be `600`) and key strength (RSA >= 2048 bits). Reports any issues.

## Usage

```bash
./src/audit_ssh_keys.sh [directory]
```

- If no directory is provided, defaults to `$HOME/.ssh`.
- The script prints a summary of each key and highlights problems with permissions or weak RSA keys.

## Example

```bash
$ ./src/audit_ssh_keys.sh ~/.ssh
Scanning SSH keys in /home/user/.ssh...
⚠️  Permissions for /home/user/.ssh/old_key are 644, should be 600
🔑 /home/user/.ssh/id_rsa: 4096 bits RSA
✅ All SSH keys look good!
```
