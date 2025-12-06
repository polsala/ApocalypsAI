# Nightly Data Debris Decryptor

## Overview

In the chaotic aftermath, fragments of data often surface, encoded or obscured by the ravages of time and digital decay. The `Nightly Data Debris Decryptor` is a whimsical-yet-useful utility designed to sift through these digital remnants and attempt to restore them to a readable state. It automatically tries common decoding methods to reveal the hidden messages within the data debris.

## Features

*   **Multi-Codec Support**: Automatically attempts to decode strings using Base64, URL-decoding, and ROT13.
*   **Simple CLI**: Easy to use from the command line with a single argument.
*   **Self-Contained**: No external dependencies beyond Python's standard library.

## Usage

To use the decryptor, simply run the `decryptor.py` script with the encoded string as an argument:

```bash
python src/decryptor.py "SGVsbG8sIEFwb2NhbHlwc0FJIQ=="
```

**Example Output:**

```
Successfully decrypted using Base64:
Hello, ApocalypsAI!
```

**Another Example (URL-encoded):**

```bash
python src/decryptor.py "Data%20with%20spaces%20%26%20symbols%21"
```

**Example Output:**

```
Successfully decrypted using URL-decode:
Data with spaces & symbols!
```

**Example (ROT13):**

```bash
python src/decryptor.py "Gur dhvpx oebja sbk whzcf bire gur ynml qbt."
```

**Example Output:**

```
Successfully decrypted using ROT13:
The quick brown fox jumps over the lazy dog.
```

If no known decoding method works, the utility will report that it could not decrypt the string and print the original input.

## Development

The `decryptor.py` script is written in Python 3.11 and uses only standard library modules (`base64`, `urllib.parse`, `codecs`, `sys`).

### Running Tests

To run the automated tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_decryptor.py
```

The tests are deterministic and offline, using `unittest.mock` to simulate command-line arguments and capture standard output for verification.
