# Mood Emoji Mapper

**What it does**

`mood-emoji-mapper` takes a short textual description of a mood (e.g., "happy", "feeling sad", "excited about the release") and returns a single Unicode emoji that best represents that mood. The mapping is performed locally with a tiny keyword‑based heuristic—no network calls, no heavy models.

**Why it’s useful**

- Add a playful touch to commit messages, CI logs, or chat bot replies.
- Completely offline and deterministic.
- Zero third‑party dependencies beyond the Python standard library.

**Installation**

```bash
# From the repository root
cd utils/mood-emoji-mapper
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, but kept for consistency)
```

**Usage**

```bash
python -m src.mapper "I am feeling ecstatic about the new feature!"
# Output: 🚀
```

Or import the function in your own code:

```python
from src.mapper import map_mood_to_emoji
emoji = map_mood_to_emoji("Just a bit tired after the marathon")
print(emoji)  # 😴
```

**Running the tests**

```bash
pytest -q
```

**Design notes**

- The mapping table lives in `src/mapper.py` and can be extended easily.
- The heuristic first normalises the input to lower‑case and then looks for the first matching keyword.
- If no keyword matches, a neutral face `😐` is returned.
