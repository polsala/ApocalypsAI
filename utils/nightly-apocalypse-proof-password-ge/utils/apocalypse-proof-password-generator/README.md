# Apocalypse-Proof Password Generator

## Overview

In a world teetering on the brink, where rogue AIs might one day attempt to brute-force your digital strongholds, the 'Apocalypse-Proof Password Generator' is your last line of defense. This whimsical-yet-robust utility crafts passwords that are not only incredibly strong but also surprisingly memorable, using a unique pattern of adjectives, nouns, numbers, and symbols.

It's designed to generate passwords that are long, complex, and resistant to dictionary attacks, ensuring your secrets remain safe even when the digital dust settles.

## Features

*   **Structured Complexity**: Generates passwords following a fixed `ADJECTIVE-NOUN-DIGITS-SYMBOL-ADJECTIVE-NOUN` pattern.
*   **High Entropy**: Utilizes Python's `secrets` module for cryptographically strong randomness.
*   **Memorable**: The word-based structure aids in recall, even under duress.
*   **CLI Interface**: Easy to use from your terminal with configurable digits and symbols.

## Installation

This utility is self-contained and requires Python 3.8+.

1.  Navigate to the utility's directory:
    ```bash
    cd utils/apocalypse-proof-password-generator
    ```
2.  Run the script directly:
    ```bash
    python src/password_generator.py
    ```

## Usage

Simply run the script without arguments to generate a default password (2 digits, 1 symbol):

```bash
python src/password_generator.py
```

Example Output:

```
Your Apocalypse-Proof Password: Ancient-Relic-93-$-Cosmic-Dust
```

You can customize the number of digits and symbols using command-line arguments:

```bash
# Generate with 3 digits and 2 symbols
python src/password_generator.py --num-digits 3 --num-symbols 2
```

Example Output for `num-digits 3` and `num-symbols 2`:

```
Your Apocalypse-Proof Password: Shadowy-Portal-123-@#-Mystic-Cipher
```

### Options

*   `--num-digits <int>`: Specify the number of digits to include (default: 2, minimum: 1).
*   `--num-symbols <int>`: Specify the number of symbols to include (default: 1, minimum: 1).
