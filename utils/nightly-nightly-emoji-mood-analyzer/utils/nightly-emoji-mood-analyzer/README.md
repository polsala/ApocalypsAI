# Nightly Emoji Mood Analyzer

**What it does**

- Parses a string (or a file) and counts a small set of emojis.
- Determines the *dominant* mood among:
  - `happy`  – 😊 😄 😁
  - `sad`    – 😢 😞 😔
  - `angry`  – 😠 😡
  - `neutral` – when none of the above are present or counts are tied.
- Provides a tiny CLI for quick one‑liners.

**Why it’s useful**

- Gives developers a playful way to gauge the emotional tone of commit messages, issue comments, or any free‑form text.
- Completely offline, deterministic, and has zero third‑party runtime dependencies beyond the Python standard library.

**Installation & Usage**

```bash
# Clone the repo (or copy the folder) and run the module directly
python -m utils.nightly-emoji-mood-analyzer src/analyzer.py "Your text here"
```

Or use it as a library:

```python
from utils.nightly_emoji_mood_analyzer.src.analyzer import analyze_mood
mood = analyze_mood("I love this! 😊😊")
print(mood)  # -> happy
```

**Testing**

Run the bundled pytest suite:

```bash
pytest utils/nightly-emoji-mood-analyzer/tests
```
