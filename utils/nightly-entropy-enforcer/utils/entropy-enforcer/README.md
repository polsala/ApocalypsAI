# Entropy Enforcer

A command-line utility designed to generate high-entropy random strings, suitable for passwords, API keys, and other security tokens. It offers flexible customization for length, character sets, and the exclusion of visually ambiguous characters.

## Features

*   **Customizable Length**: Specify the desired length of the generated string.
*   **Character Set Control**: Include or exclude digits, lowercase letters, uppercase letters, and symbols.
*   **Ambiguity Exclusion**: Option to remove characters that can be easily confused (e.g., `l`, `I`, `O`, `0`, `1`).
*   **Cryptographically Secure**: Utilizes Python's `secrets` module for strong randomness.

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

To use it, simply navigate to the `utils/entropy-enforcer/src/` directory and run `enforcer.py`.

## Usage

```bash
python src/enforcer.py [OPTIONS]
```

### Examples

1.  **Generate a default 16-character string (digits, lower, upper):**
    ```bash
    python src/enforcer.py
    ```

2.  **Generate a 24-character string including symbols:**
    ```bash
    python src/enforcer.py --length 24 --symbols
    ```

3.  **Generate a 12-character string with only lowercase letters and digits, excluding ambiguous characters:**
    ```bash
    python src/enforcer.py --length 12 --no-upper --exclude-ambiguous
    ```

4.  **Generate a 32-character API key with only uppercase letters and digits:**
    ```bash
    python src/enforcer.py --length 32 --no-lower --no-symbols
    ```

### Options

*   `-l`, `--length <INT>`: Length of the generated string (default: `16`).
*   `--no-digits`: Exclude digits (0-9).
*   `--no-lower`: Exclude lowercase letters (a-z).
*   `--no-upper`: Exclude uppercase letters (A-Z).
*   `-s`, `--symbols`: Include symbols (`!@#$%...`).
*   `-x`, `--exclude-ambiguous`: Exclude ambiguous characters (e.g., `l`, `I`, `O`, `0`, `1`).

## Development

### Running Tests

To run the tests, navigate to the `utils/entropy-enforcer/` directory and execute:

```bash
python -m unittest tests/test_enforcer.py
```
