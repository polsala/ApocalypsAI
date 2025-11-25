# Nightly Chronicle Keeper Checksum Checker

## 📜 Purpose

In the ever-shifting sands of the post-apocalyptic digital wasteland, data integrity is paramount. The "Nightly Chronicle Keeper Checksum Checker" is a humble yet vital utility designed to help survivors (and their automated agents) ensure that their precious files remain untainted by cosmic rays, rogue bit-flips, or mischievous digital gremlins.

It generates and verifies SHA256 checksums, acting as a digital guardian for your most cherished chronicles, blueprints, and cat memes.

## ✨ Features

*   **Generate Checksums**: Compute SHA256 hashes for any file.
*   **Save Checksums**: Store checksums either in a `.sha256` sidecar file or append them to a central manifest file.
*   **Verify Integrity**: Compare a file's current checksum against a previously recorded one to detect any changes.
*   **Simple CLI**: Easy to integrate into scripts or use directly from the command line.

## 🚀 Usage

This utility is a Python 3.11 script.

### Prerequisites

*   Python 3.11 or higher

### Commands

#### Generate a checksum

To generate a checksum for a file and save it to a `.sha256` file next to it:

```bash
python src/checksum_checker.py generate path/to/your/important_document.txt
```

This will create `path/to/your/important_document.txt.sha256` containing the checksum.

To generate a checksum and append it to a central manifest file:

```bash
python src/checksum_checker.py generate path/to/your/another_file.jpg --manifest my_chronicle_manifest.sha256
```

If `my_chronicle_manifest.sha256` doesn't exist, it will be created. Otherwise, the new entry will be appended.

#### Verify a checksum

To verify a file against a known SHA256 checksum:

```bash
python src/checksum_checker.py verify path/to/your/important_document.txt <expected_sha256_checksum>
```

Replace `<expected_sha256_checksum>` with the actual 64-character SHA256 hash.

Example:
```bash
python src/checksum_checker.py verify my_data.zip 8e2e0f2a4b7c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e
```

The utility will print whether the verification was successful or if the file has been tampered with. It will exit with `0` for success and `1` for failure.

## 🛠️ Development

### Running Tests

To ensure the Chronicle Keeper is in top shape, run its self-contained tests:

```bash
python -m unittest tests/test_checksum_checker.py
```

All tests are deterministic and do not interact with the actual filesystem or network, relying on mocks for isolation.
