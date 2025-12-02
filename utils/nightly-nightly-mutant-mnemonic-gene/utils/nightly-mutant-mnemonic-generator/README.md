# Nightly Mutant Mnemonic Generator

## Overview

The `nightly-mutant-mnemonic-generator` is a whimsical yet practical command-line utility designed to help you create strong, memorable passphrases. Instead of struggling with random strings of characters, this tool generates passphrases using a curated list of post-apocalyptic themed words, making them easier to recall while still providing robust security.

It's perfect for those who need to remember complex passwords in a world where digital notes might be scarce or compromised.

## Features

*   **Memorable Passphrases**: Generates passphrases from a unique dictionary of themed words.
*   **Configurable Length**: Specify the number of words in your passphrase.
*   **Custom Separators**: Choose your preferred word separator (e.g., hyphens, spaces, underscores).
*   **Cryptographically Secure**: Uses Python's `secrets` module for robust randomness when no seed is provided.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Installation

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-mutant-mnemonic-generator
    ```
2.  The utility is a standalone Python script. No special installation is required beyond having Python 3.11+ installed.

## Usage

Run the `generator.py` script from its directory:

```bash
python src/generator.py --words 4 --separator "-"
```

### Arguments:

*   `--words <int>`: The number of words to include in the passphrase. (Default: 4)
*   `--separator <string>`: The character(s) to use between words. (Default: `-`)
*   `--seed <int>`: (Optional) A numeric seed for deterministic generation. **Do not use for actual security; only for testing.**

### Examples:

Generate a 5-word passphrase with spaces:
```bash
python src/generator.py --words 5 --separator " "
```

Generate a 3-word passphrase with underscores:
```bash
python src/generator.py --words 3 --separator "_"
```

Generate a passphrase for testing with a specific seed:
```bash
python src/generator.py --words 4 --separator "-" --seed 123
```

## Development and Testing

To run the tests, navigate to the utility's directory and execute:

```bash
python -m unittest tests/test_generator.py
```

Tests are designed to be deterministic and self-contained, using mocks for file I/O and randomness to ensure consistent results.
