# Mock rationale: No external services are called; tests are fully deterministic.

import os
import sys
import unittest
from uuid import UUID

# Add the src directory to ``sys.path`` so we can import the module under test.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from shortener import encode_uuid, decode_uuid


class TestUUIDShortener(unittest.TestCase):
    def test_encode_decode_roundtrip(self):
        """Encode a UUID and then decode it, expecting the original value."""
        original = "123e4567-e89b-12d3-a456-426614174000"
        short = encode_uuid(original)
        restored = decode_uuid(short)
        self.assertEqual(UUID(original), UUID(restored))

    def test_known_encoding(self):
        """Validate encoding against known edge‑case UUIDs."""
        # The smallest non‑zero UUID should encode to "1"
        uuid_min = "00000000-0000-0000-0000-000000000001"
        self.assertEqual(encode_uuid(uuid_min), "1")

        # The maximum UUID (2**128‑1) should produce a 22‑character Base‑62 string.
        uuid_max = "ffffffff-ffff-ffff-ffff-ffffffffffff"
        short_max = encode_uuid(uuid_max)
        self.assertEqual(len(short_max), 22)
        # Decoding must return the original max UUID.
        self.assertEqual(decode_uuid(short_max), uuid_max)


if __name__ == "__main__":
    unittest.main()
