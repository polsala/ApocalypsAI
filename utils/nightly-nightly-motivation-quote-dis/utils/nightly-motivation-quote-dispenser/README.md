# Nightly Motivation Quote Dispenser

Provides a whimsical yet useful utility that prints a random motivational quote from a curated list. Can be used as a CLI (`python -m nightly-motivation-quote-dispenser`) or imported as a module.

## Usage

```bash
python -m nightly-motivation-quote-dispenser
# or
from nightly_motivation_quote_dispenser import get_random_quote
print(get_random_quote())
```

## Design

- Self‑contained, no external network calls.
- Deterministic tests using mocks.
