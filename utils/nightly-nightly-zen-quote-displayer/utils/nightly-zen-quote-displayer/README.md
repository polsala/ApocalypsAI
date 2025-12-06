# Nightly Zen Quote Displayer

A tiny, whimsical utility that prints a random Zen quote to your terminal. Optionally includes a simple ASCII art meditation cushion.

## Features

- Deterministic offline operation (no network calls).
- `--art` flag to add calming ASCII art.
- Lightweight, zero external dependencies.

## Usage

```sh
python -m src.zen          # prints a random quote
python -m src.zen --art    # prints quote with art
```

## Testing

Run the bundled tests with:

```sh
python -m unittest discover -s tests
```
