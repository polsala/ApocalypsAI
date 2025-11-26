# Survival Cache Checksum Verifier

Ensures your digital survival caches haven't been corrupted by cosmic rays, bit rot, or mischievous digital gremlins. This utility verifies the integrity of files in a specified directory against a manifest of expected SHA256 checksums.

## 🚀 Usage

```bash
python src/verifier.py <cache_directory> <manifest_file>
```

- `<cache_directory>`: The path to the directory containing the files you want to verify.
- `<manifest_file>`: The path to a JSON file containing the expected SHA256 checksums.

### Example

Let's say you have a cache directory structure like this:

```
my_survival_cache/
├── important_document.txt
└── logs/
    └── activity.log
```

And your `manifest.json` looks like this:

```json
{
  "important_document.txt": "a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890",
  "logs/activity.log": "f0e9d8c7b6a54321f0e9d8c7b6a54321f0e9d8c7b6a54321f0e9d8c7b6a54321"
}
```

You would run the verifier like this:

```bash
python src/verifier.py my_survival_cache manifest.json
```

The utility will output the status of each file and a final summary.

## ✨ Features

-   **SHA256 Checksum Verification**: Uses robust SHA256 hashing to detect any changes.
-   **JSON Manifest Support**: Easily define expected checksums for your files.
-   **Missing File Detection**: Identifies files present in the manifest but missing from the cache.
-   **Corrupted File Detection**: Flags files whose actual checksum does not match the expected one.
-   **Self-Contained**: No external dependencies beyond Python's standard library.

## 🛠️ Development

### Running Tests

To ensure the verifier is functioning correctly, run the provided unit tests:

```bash
python -m unittest tests/test_verifier.py
```

### Manifest Format

The manifest file must be a JSON object where:
-   Keys are file paths relative to the `cache_directory`.
-   Values are the expected SHA256 checksums (64-character hexadecimal strings).

Example:
```json
{
  "path/to/file1.txt": "expected_sha256_checksum_for_file1",
  "another_file.bin": "expected_sha256_checksum_for_another_file"
}
```

## 📜 License

This utility is provided under the [MIT License](LICENSE).
