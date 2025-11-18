# Nightly Chronicle Keeper Checksum Checker

In a world where data integrity is paramount, the Chronicle Keeper's Checksum Checker ensures your precious files remain untainted. This utility allows you to generate SHA256 checksums for any file and later verify them, safeguarding your digital chronicles against corruption, accidental modification, or the insidious byte-rot of the apocalypse.

## Features

*   **Generate Checksum**: Compute the SHA256 hash for a given file.
*   **Verify Checksum**: Compare a file's current hash against a previously recorded one.
*   **Simple CLI**: Easy to use from the command line.

## Usage

### Generate a Checksum

To generate a checksum for a file:

```bash
python src/checksum_checker.py generate <path_to_file>
```

Example:
```bash
python src/checksum_checker.py generate my_important_data.txt
# Output: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938798a0 my_important_data.txt
```

### Verify a Checksum

To verify a file against a known checksum:

```bash
python src/checksum_checker.py verify <path_to_file> <expected_checksum>
```

Example:
```bash
python src/checksum_checker.py verify my_important_data.txt 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938798a0
# Output: Verification successful for my_important_data.txt
```

If the checksums do not match:
```bash
python src/checksum_checker.py verify my_important_data.txt wrong_checksum
# Output: Verification failed for my_important_data.txt. Expected: wrong_checksum, Got: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938798a0
```

## Development

This utility is written in Python 3.11 and has no external dependencies beyond the standard library.

### Running Tests

```bash
python -m unittest tests/test_checksum_checker.py
```
