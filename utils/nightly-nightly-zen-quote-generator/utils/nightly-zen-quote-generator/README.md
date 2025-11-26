# Nightly Zen Quote Generator

A whimsical utility that prints a random Zen‑inspired quote. Useful for adding a moment of calm to scripts, CI logs, or terminal sessions.

## Features

- **Offline** – no network calls, all quotes are bundled.
- **Deterministic** – supply `--seed` to get the same quote every time.
- **Simple CLI** – run with `python -m zen_quote [--seed N]`.

## Installation

Just copy the folder into your repository; the utility only depends on the Python standard library.

## Usage

```bash
python -m zen_quote            # random quote
python -m zen_quote --seed 42   # reproducible quote
```
