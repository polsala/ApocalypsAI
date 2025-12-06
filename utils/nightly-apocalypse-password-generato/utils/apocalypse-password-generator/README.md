# Apocalypse Password Generator

## Overview

In the grim darkness of the far future, or perhaps just a Tuesday, your digital defenses are paramount. The Apocalypse Password Generator is a whimsical-yet-critical utility designed to forge robust, uncrackable passwords and memorable, themed passphrases to safeguard your most precious data from rogue AIs, data raiders, and existential threats.

Whether you need a high-entropy string for your bunker's access panel or a memorable phrase for your emergency broadcast system, this tool has you covered.

## Features

*   **Random Password Generation**: Create strong, cryptographically secure passwords with customizable length and character sets (lowercase, uppercase, digits, symbols).
*   **Apocalypse Passphrase Mode**: Generate memorable passphrases using a curated dictionary of post-apocalyptic and survival-themed words. Perfect for when you need something strong but also easy to recall under duress.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Installation

This utility is self-contained. Simply navigate to the `utils/apocalypse-password-generator/` directory.

## Usage

### Random Password Generation

To generate a random password, run the `password_generator.py` script directly:

```bash
python src/password_generator.py --mode random --length 16 --digits --symbols --uppercase --lowercase
```

**Options for `random` mode:**
*   `--length <int>`: Desired password length (default: 12).
*   `--digits`: Include digits (0-9).
*   `--symbols`: Include common symbols (!@#$%^&*()_-+=[]{}|;:,.<>?).
*   `--uppercase`: Include uppercase letters (A-Z).
*   `--lowercase`: Include lowercase letters (a-z).
*   (If no character type is specified, all types are included by default).

### Apocalypse Passphrase Generation

To generate a themed passphrase:

```bash
python src/password_generator.py --mode passphrase --words 4 --separator "-"
```

**Options for `passphrase` mode:**
*   `--words <int>`: Number of words in the passphrase (default: 4).
*   `--separator <char>`: Character to use between words (default: `-`).

### Examples

*   Generate a 20-character random password with all character types:
    `python src/password_generator.py --mode random --length 20`
*   Generate a 10-character password with only lowercase and digits:
    `python src/password_generator.py --mode random --length 10 --lowercase --digits`
*   Generate a 5-word passphrase separated by spaces:
    `python src/password_generator.py --mode passphrase --words 5 --separator " "`

## Development & Testing

To run tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_password_generator.py
```
