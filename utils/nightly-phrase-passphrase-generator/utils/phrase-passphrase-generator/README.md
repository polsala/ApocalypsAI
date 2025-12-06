# Phrase Passphrase Generator

A tiny, self‑contained utility that turns a memorable **phrase** and a **salt** into a reproducible password.

## Features
- Pure‑Python, no third‑party packages.
- Deterministic output – the same inputs always give the same password.
- Adjustable length and character‑set (`alnum`, `alpha`, `numeric`).
- Small CLI for quick use from the terminal.

## Installation
```bash
# From the repository root
cd utils/phrase-passphrase-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty – only stdlib)
```

## Usage (CLI)
```bash
python -m src.generator \
    --phrase "my secret phrase" \
    --salt "apocalypse" \
    --length 20 \
    --charset alnum
```

## API
```python
from src.generator import generate_password

pwd = generate_password(
    phrase="openai",
    salt="apocalypse",
    length=12,
    charset="alnum",
)
print(pwd)  # → openaiapocal
```

## Testing
```bash
pytest -q
```

---
*Created by the ApocalypsAI Nightly Integrator.*
