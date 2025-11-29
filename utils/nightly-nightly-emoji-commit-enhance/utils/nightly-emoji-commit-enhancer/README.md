# Nightly Emoji Commit Enhancer

A whimsical yet practical utility that appends a random emoji to your Git commit messages, keeping them under the classic 72‑character limit.

## Features

- **Random emoji** from a curated list of friendly symbols.
- **Deterministic mode** via `--seed` for reproducible results (useful for testing or CI).
- **Length‑aware**: truncates the original message if needed so the final string (message + space + emoji) never exceeds 72 characters.
- **Zero external dependencies** – pure Python 3.11 standard library.

## Installation

```bash
# From the repository root
python -m pip install .
```

*(The utility is self‑contained; no extra packages are required.)*

## Usage

```bash
# Pipe a message
echo "Refactor authentication flow" | python -m utils.nightly-emoji-commit-enhancer.src.enhancer

# Or pass it directly
python -m utils.nightly-emoji-commit-enhancer.src.enhancer --message "Add unit tests for payment module"

# Deterministic mode (same seed → same emoji)
python -m utils.nightly-emoji-commit-enhancer.src.enhancer --message "Fix typo" --seed 42
```

## Development

Run the test suite with:

```bash
python -m unittest discover utils/nightly-emoji-commit-enhancer/tests
```
