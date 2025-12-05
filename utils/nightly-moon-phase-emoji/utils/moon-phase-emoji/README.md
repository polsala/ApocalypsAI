# Moon Phase Emoji

**What it does**

`moon-phase-emoji` is a self‑contained Python 3.11 utility that, given a `datetime.date`, returns the appropriate moon‑phase emoji (🌑, 🌒, 🌓, 🌔, 🌕, 🌖, 🌗, 🌘). It works entirely offline – no external APIs – and can be used as a library or a tiny CLI.

**Why it’s useful**

- Add a visual cue to daily reports, commit messages, or chat bots.
- No network calls, so it’s safe for CI environments.
- Deterministic algorithm based on Conway’s method, guaranteeing the same output for the same date.

**Installation**

```bash
# Clone the repository and navigate to the utility folder
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/moon-phase-emoji
# (Optional) create a virtual environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # No extra deps needed
```

**Usage as a library**

```python
from src.moon_phase import get_moon_phase_emoji
from datetime import date

print(get_moon_phase_emoji(date(2025, 11, 30)))  # 🌕
```

**CLI usage**

```bash
python -m src.moon_phase 2025-11-30
# Output: 🌕
```

**Running the tests**

```bash
python -m unittest discover -s tests
```
