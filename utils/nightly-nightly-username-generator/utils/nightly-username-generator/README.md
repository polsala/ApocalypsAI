# Nightly Username Generator

A tiny, self‑contained utility that creates fun, deterministic usernames.

## Features
- No external dependencies (uses only the Python standard library).
- Deterministic output – the same seed always yields the same username.
- Simple CLI for quick ad‑hoc usage.

## Usage
```bash
python -m nightly_username_generator.generate --seed 42
# → brave‑wizard042
```

Or import the function in your own code:
```python
from nightly_username_generator.generator import generate_username

print(generate_username(seed=42))  # deterministic output
```

## How it works
The generator hashes the provided seed with SHA‑256, then maps portions of the hash to:
1. An adjective from a short curated list.
2. A noun from a short curated list.
3. A three‑digit number (0‑999).

Because the process is pure‑function and only depends on the seed, it is fully deterministic and perfect for unit testing.
