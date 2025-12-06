# Nightly Apocalypse Cryptic Scrambler

A whimsical utility that lets you encrypt and decrypt short messages using a fixed, post‑apocalyptic substitution cipher. Perfect for leaving secret notes in a bunker or adding a touch of mystery to your survival journal.

## Features

* **Deterministic** – the same plain‑text always maps to the same cipher‑text.
* **Case‑preserving** – upper‑case stays upper‑case, lower‑case stays lower‑case.
* **CLI** – quick one‑liners:
  ```bash
  python -m src.scrambler -e "Stay hidden"
  python -m src.scrambler -d "Uqz qzvgr"
  ```

## How it works

Each letter A‑Z is mapped to another letter according to a hard‑coded table (see `scrambler.py`). Non‑alphabetic characters are left untouched.

## Installation & testing

```bash
# From the repository root
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # No extra deps needed
python -m unittest discover -s utils/nightly-apocalypse-cryptic-scrambler/tests
```

Enjoy encrypting your apocalypse‑era secrets!
