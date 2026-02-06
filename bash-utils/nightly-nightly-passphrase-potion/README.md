# nightly-passphrase-potion

**A whimsical Bash utility that brews a magical passphrase**

## Overview
`nightly-passphrase-potion` creates a four‑word passphrase, each word capitalised, and stitches them together with random (or deterministic) symbols.  The result looks like a potion recipe – perfect for a quick, memorable, yet strong password.

## Features
- Uses a supplied word list or falls back to `/usr/share/dict/words`.
- Optional `--seed` flag for deterministic output (useful for testing or repeatable recipes).
- Customisable symbol set (default: `! @ # $ % & * ?`).
- Fully self‑contained Bash script – no external dependencies.

## Installation
```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-passphrase-potion
chmod +x src/passphrase.sh
```

## Usage
```bash
# Random passphrase (default word list)
./src/passphrase.sh

# Use a custom word list
./src/passphrase.sh --list mywords.txt

# Deterministic passphrase for testing or repeatable recipes
./src/passphrase.sh --list mywords.txt --seed 42
```

## Example Output
```
Mystic!Dragon@Phoenix#Unicorn
```

## Testing
Run the bundled test suite with Bash:
```bash
cd tests
bash test_passphrase.sh
```
All tests should pass.
