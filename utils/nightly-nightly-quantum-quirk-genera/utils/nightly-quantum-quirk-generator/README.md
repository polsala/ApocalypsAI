# Nightly Quantum Quirk Generator

A whimsical-yet-useful utility for generating secure and memorable passphrases, perfect for safeguarding your digital stashes in the post-apocalyptic wasteland.

## Purpose

In a world of digital decay and lurking data scavengers, strong passphrases are your first line of defense. The Quantum Quirk Generator crafts unique, multi-word passphrases that are both robust against brute-force attacks and easy for a human to remember. It uses a cryptographically secure random number generator and can draw from a default apocalyptic-themed wordlist or a custom one you provide.

## Usage

The utility is a Python 3.11 script.

### Prerequisites

*   Python 3.11 or higher

### Running the Generator

Navigate to the `src` directory and run the `generator.py` script:

```bash
python src/generator.py [OPTIONS]
```

### Options

*   `-n`, `--num-words <int>`: The number of words to include in the passphrase (default: 4, range: 3-10).
*   `-s`, `--separator <str>`: The character(s) to use between words (default: `-`).
*   `-w`, `--wordlist-file <path>`: Path to a custom wordlist file (one word per line). If not provided, a default apocalyptic-themed list is used.

### Examples

1.  **Generate a default 4-word passphrase:**
    ```bash
    python src/generator.py
    # Example output: bunker-radiation-glitch-survival
    ```

2.  **Generate a 5-word passphrase with a custom separator:**
    ```bash
    python src/generator.py -n 5 -s "_"
    # Example output: wasteland_echo_mutant_cipher_quirk
    ```

3.  **Generate a passphrase using a custom wordlist:**
    First, create a file named `my_words.txt` with words like this:
    ```
    secure
    vault
    data
    shield
    secret
    key
    ```
    Then run:
    ```bash
    python src/generator.py -n 3 -w my_words.txt
    # Example output: secure-key-vault
    ```

## Development & Testing

### Running Tests

To ensure the generator is functioning correctly and securely, run the provided tests. Navigate to the `tests` directory and execute:

```bash
python -m unittest discover -s tests
```

The tests are designed to be deterministic and offline, using mocks for `random.SystemRandom` and file operations to ensure consistent results.

## License

This utility is released under the MIT License. See the main repository's `LICENSE` file for details.
