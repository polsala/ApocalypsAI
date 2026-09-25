# nightly-ssh-key-audit

A tiny Bash utility that scans your SSH private keys and warns about keys smaller than 2048 bits. Useful for hardening your workstation before a post‑apocalypse.

## Usage

```sh
./src/ssh_key_audit.sh [directory]
```

If no directory is given, defaults to `~/.ssh`.

The script prints each key path and its size, and highlights weak keys.

## Exit codes

- **0**: No weak keys found
- **1**: At least one weak key detected
- **2**: Error (e.g., directory not found)

## Testing

Run `bash tests/test_ssh_key_audit.sh` to execute the deterministic test suite.
