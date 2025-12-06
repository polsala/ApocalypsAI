# Chronos-Sync Checksum Buddy

## 🕰️✨ Your Digital Integrity Guardian

The Chronos-Sync Checksum Buddy is a whimsical yet essential utility designed to help you maintain the integrity of your files across the temporal continuum. Whether you're verifying downloads, checking for accidental modifications, or just ensuring your critical configuration files haven't been tampered with, this buddy has your back. It generates and verifies cryptographic checksums (SHA256 and MD5) for any given file.

## 🚀 Features

*   **Generate Checksum**: Compute the SHA256 or MD5 hash of a file.
*   **Verify Checksum**: Compare a file's current hash against a known hash value.
*   **Algorithm Choice**: Select between SHA256 (default) and MD5.

## 🛠️ Usage

This utility is a Python 3.11+ script. You can run it directly from the command line.

### Generate a Checksum

To generate the SHA256 checksum for a file:

```bash
python3 utils/chronos-sync-checksum-buddy/src/checksum_buddy.py generate --file /path/to/your/file.txt
```

To generate an MD5 checksum:

```bash
python3 utils/chronos-sync-checksum-buddy/src/checksum_buddy.py generate --file /path/to/your/file.txt --algorithm md5
```

### Verify a Checksum

To verify a file against a known SHA256 checksum:

```bash
python3 utils/chronos-sync-checksum-buddy/src/checksum_buddy.py verify --file /path/to/your/file.txt --expected-checksum <your_sha256_hash_here>
```

To verify against a known MD5 checksum:

```bash
python3 utils/chronos-sync-checksum-buddy/src/checksum_buddy.py verify --file /path/to/your/file.txt --expected-checksum <your_md5_hash_here> --algorithm md5
```

### Examples

```bash
# Generate SHA256 for a README
python3 utils/chronos-sync-checksum-buddy/src/checksum_buddy.py generate --file README.md
# Output: 5f4dcc3b5aa765d61d8327deb882cf99 (example hash)

# Verify a downloaded archive
python3 utils/chronos-sync-checksum-buddy/src/checksum_buddy.py verify --file my_archive.zip --expected-checksum 0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b
# Output: Checksum MATCHES!

# Verify a critical config file with MD5
python3 utils/chronos-sync-checksum-buddy/src/checksum_buddy.py verify --file config.ini --expected-checksum d41d8cd98f00b204e9800998ecf8427e --algorithm md5
# Output: Checksum MISMATCH! Expected: d41d8cd98f00b204e9800998ecf8427e, Got: abcdef1234567890abcdef1234567890
```

## 🧪 Testing

To run the tests for Chronos-Sync Checksum Buddy:

```bash
python3 -m unittest utils/chronos-sync-checksum-buddy/tests/test_checksum_buddy.py
```
