import base64
import hashlib
import sys
from typing import Dict


def _format_md5(digest: bytes) -> str:
    """Return MD5 fingerprint in colon‑separated hex format."""
    return ":".join(f"{b:02x}" for b in digest)


def _format_sha256(digest: bytes) -> str:
    """Return SHA256 fingerprint in base64 format prefixed with 'SHA256:' as OpenSSH does."""
    b64 = base64.b64encode(digest).decode("ascii")
    return f"SHA256:{b64}"


def compute_fingerprints(public_key: str) -> Dict[str, str]:
    """Compute MD5 and SHA256 fingerprints for an OpenSSH public key.

    Args:
        public_key: The full public‑key string (e.g. ``"ssh-rsa AAAAB3... user@host"``).
    Returns:
        A dict with ``"md5"`` and ``"sha256"`` keys.
    """
    parts = public_key.strip().split()
    if len(parts) < 2:
        raise ValueError("Invalid SSH public key format")
    key_body = parts[1]
    try:
        key_bytes = base64.b64decode(key_body)
    except Exception as exc:
        raise ValueError("Base64 decoding of key failed") from exc

    md5_hash = hashlib.md5()
    md5_hash.update(key_bytes)
    md5_fp = _format_md5(md5_hash.digest())

    sha256_hash = hashlib.sha256()
    sha256_hash.update(key_bytes)
    sha256_fp = _format_sha256(sha256_hash.digest())

    return {"md5": md5_fp, "sha256": sha256_fp}


def _cli():
    if len(sys.argv) != 2:
        print("Usage: python -m src.fingerprint \"<public_key_string>\"")
        sys.exit(1)
    key = sys.argv[1]
    try:
        fps = compute_fingerprints(key)
        print(f"MD5:    {fps['md5']}")
        print(f"SHA256: {fps['sha256']}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    _cli()
