import hashlib
import base64
from src.fingerprint import compute_fingerprints


def test_compute_fingerprints_mock(monkeypatch):
    """Deterministic test using mocked hash functions.

    # Mock rationale: replace hashlib's md5 and sha256 with dummy objects that
    # always return a predictable 16‑byte digest (bytes 0x01‑0x10). This makes the
    # test offline, deterministic, and independent of the actual key content.
    """

    class DummyHash:
        def __init__(self):
            pass
        def update(self, _data):
            pass
        def digest(self):
            # 16 bytes: 0x01, 0x02, ..., 0x10
            return bytes(range(1, 17))

    # Patch hashlib.md5 and hashlib.sha256 to return DummyHash instances
    monkeypatch.setattr(hashlib, "md5", lambda: DummyHash())
    monkeypatch.setattr(hashlib, "sha256", lambda: DummyHash())

    # Example public key (the actual content is irrelevant due to mocking)
    key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCt user@example.com"
    result = compute_fingerprints(key)

    expected_fp = "01:02:03:04:05:06:07:08:09:0a:0b:0c:0d:0e:0f:10"
    assert result["md5"] == expected_fp
    # SHA256 fingerprint uses the same dummy digest but is base64‑encoded
    # bytes 0x01‑0x10 => base64 "AQIDBAUGBwgJCgsMDQ4PEA=="
    expected_sha256 = "SHA256:AQIDBAUGBwgJCgsMDQ4PEA=="
    assert result["sha256"] == expected_sha256
