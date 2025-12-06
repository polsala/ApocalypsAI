# Nightly Moon Phase Emoji

A tiny, self‑contained Python utility that tells you the moon phase for any calendar date and returns a friendly emoji representation.

## Features
- Pure Python 3.11, no external dependencies.
- Deterministic algorithm (no network calls, no randomness).
- Provides both a human‑readable phase name and the matching emoji.
- Includes a simple CLI for quick command‑line use.

## Usage
```bash
python -m utils.nightly-moon-phase-emoji.src.moon_phase 2025-11-16
# Output: Full Moon 🌕
```

Or as a library:
```python
from utils.nightly-moon-phase-emoji.src.moon_phase import get_moon_phase
from datetime import date

phase, emoji = get_moon_phase(date.today())
print(f"{phase} {emoji}")
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-moon-phase-emoji/tests
```

---
*Created by the ApocalypsAI Nightly Integrator.*
