# Nightly Emoji Mood Meter

**What it does**

`nightly-emoji-mood-meter` scans a short piece of text and returns a single emoji that best represents the overall mood. It uses a lightweight keyword‑based approach, so it works completely offline and has zero runtime dependencies beyond the Python standard library.

**Why it’s useful**

- Add a quick visual cue to commit messages, CI logs, or chat bot replies.
- Fun way to surface sentiment in small‑scale scripts without pulling in heavy NLP libraries.
- Perfect for the nightly‑integrator’s whimsical spirit while still being practical.

**Installation**

```bash
# From the repository root
cd utils/nightly-emoji-mood-meter
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Usage**

```bash
# As a module
python -m src.mood_meter "I love this new feature!"
# → 😄

# Or import in your own code
from src.mood_meter import get_mood_emoji
emoji = get_mood_emoji("The build failed again…")
print(emoji)  # → 😞
```

**Running the tests**

```bash
pytest -q
```

---

*Created by the ApocalypsAI Nightly Integrator.*
