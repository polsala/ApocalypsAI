# Nightly Emoji Mood Tracker

**What it does**

`emoji-mood-tracker` maps a human‑readable mood description (e.g., "happy", "frustrated") to a single Unicode emoji that best represents that feeling. It can be used in:

- Commit messages to convey the author's emotional state.
- Pull‑request titles for a dash of personality.
- Daily stand‑up notes or chat bots.

**Features**

- Zero external dependencies – pure Python 3.11.
- Extensible mapping dictionary (easy to add new moods).
- Simple CLI: `python -m mood_tracker <mood>` prints the emoji.
- Fully unit‑tested with deterministic, offline mocks.

**Installation**

```bash
# From the repository root
cd utils/nightly-emoji-mood-tracker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for future deps)
```

**Usage**

```bash
python -m src.mood_tracker happy
# => 😄
```

**Running the tests**

```bash
pytest -q
```
