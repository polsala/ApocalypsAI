# Nightly Emoji Mood Analyzer

**What it does**

- Scans a short piece of text.
- Counts occurrences of predefined positive and negative words.
- Returns an emoji representing the overall mood:
  - `😊` – more positive than negative
  - `😐` – equal or no sentiment words found
  - `😞` – more negative than positive

**Why it’s useful**

- Quick visual cue for chat bots, commit messages, or any place you want a lightweight sentiment indicator.
- No external dependencies – pure Python 3.11.
- Fully deterministic and offline‑friendly.

**Installation**

```bash
# From the repository root
cd utils/nightly-emoji-mood-analyzer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for future extensibility)
```

**Usage**

```bash
# As a module
python -m src.mood_analyzer "I love this new feature!"
# => 😊

# As a library
from src.mood_analyzer import analyze_mood
emoji = analyze_mood("Bug fixes are terrible.")
print(emoji)  # 😞
```

**Testing**

```bash
pytest -q
```

All tests run offline and use mocked word lists.
