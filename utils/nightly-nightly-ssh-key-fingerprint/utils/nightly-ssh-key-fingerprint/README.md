# SSH Key Fingerprint Utility

Generate MD5 and SHA256 fingerprints for OpenSSH public keys.

## Features
- Parses standard OpenSSH public‑key strings.
- Returns fingerprints in the familiar colon‑separated MD5 format and base64‑encoded SHA256 format.
- Small, zero‑dependency Python module (standard library only).

## Usage
```bash
python -m src.fingerprint "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC... user@example.com"
```
Will output something like:
```
MD5:    1a:2b:3c:4d:5e:6f:7a:8b:9c:0d:1e:2f:3a:4b:5c:6d
SHA256: SHA256:AbCdEfGhIjKlMnOpQrStUvWxYz1234567890abcdEFG=
```

## API
```python
from src.fingerprint import compute_fingerprints

fingerprints = compute_fingerprints(public_key_str)
# fingerprints == {"md5": "...", "sha256": "..."}
```

## Testing
Run the bundled tests with:
```bash
pytest utils/nightly-ssh-key-fingerprint/tests
```
