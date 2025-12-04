# nightly‑scrabble‑word‑finder

A tiny, offline utility that, given a bag of letters, returns every word that can be formed from those letters (using a modest built‑in Scrabble‑style word list).

## Features
- Pure Python 3.11, no external dependencies.
- Deterministic output sorted by length (longest first) then alphabetically.
- Simple CLI for quick ad‑hoc look‑ups.

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and run the module directly:
python -m utils.nightly-scrabble-word-finder.src.scrabble_finder "aple"
```

### API
```python
from utils.nightly-scrabble-word-finder.src.scrabble_finder import find_words

words = find_words("aple", min_len=2)
# → ['pale', 'plea', 'leap', 'ape', 'pea', 'pal', 'lap', 'ale', 'lea']
```

## Testing
```bash
pytest utils/nightly-scrabble-word-finder/tests
```

---
*Created by the ApocalypsAI Nightly Integrator.*
