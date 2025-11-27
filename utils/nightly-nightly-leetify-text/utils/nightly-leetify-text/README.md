# nightly‑leetify‑text

**Leetify** – turn any string into classic 1337‑speak.

## Features
- `leetify(text: str) -> str` – pure‑Python function with no external dependencies.
- Command‑line interface: `python -m leetify "Hello World"` prints the leet version.
- Fully tested with deterministic unit tests (no network calls).

## Installation
```bash
# From the repository root
cd utils/nightly-leetify-text
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (empty, stdlib only)
```

## Usage
```bash
python -m src.leetify "ApocalypsAI is awesome!"
# Output: 4p4c4lyp5AI 15 4w350m3!
```

## Development
Run the test suite with:
```bash
pytest -q
```
