# Wordle Helper

A lightweight, offline utility to help you solve Wordle (or any 5‑letter word guessing game).

## Features

- **Pattern matching**: Provide known letters with `?` for unknown positions (e.g., `c??e?`).
- **Exclusion list**: Specify letters that are known *not* to be in the word.
- **Built‑in dictionary**: No network calls – the utility ships with a curated list of common 5‑letter English words.
- **CLI**: Simple command‑line interface.

## Installation & Usage

```bash
# Clone the repository (or just copy the utils/wordle-helper folder)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # No extra deps needed

# Run the helper
python -m utils.wordle-helper.src.wordle_helper --pattern c??e? --exclude a,b,d
```

The script will print all matching words, one per line.

## Development

Run the test suite with:

```bash
python -m pytest utils/wordle-helper/tests
```

## License

MIT – see the top‑level LICENSE file.
