# Nightly Emoji Mood Logger

## Overview
`emoji-mood-logger` scans a short piece of text and returns a single emoji that best represents the overall sentiment:

- **😊** – Positive / happy
- **😢** – Negative / sad
- **😐** – Neutral / mixed or unknown

The implementation is deliberately lightweight: it uses a small handcrafted keyword list and **does not** call any external services, making it safe for offline execution and CI environments.

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and navigate into it
cd utils/nightly-emoji-mood-logger

# Run the utility directly with Python 3.11+
python -m src.logger "I just finished a great sprint!"
# → 😊
```

You can also import the core function in your own Python code:
```python
from src.logger import get_mood_emoji

emoji = get_mood_emoji("Feeling a bit down after the bug hunt.")
print(emoji)  # 😢
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
All tests are deterministic and require no network access.

## Design Rationale
- **Deterministic** – No randomness; the same input always yields the same emoji.
- **Offline‑friendly** – No external API calls; perfect for CI pipelines.
- **Extensible** – The keyword dictionaries are easy to expand for more nuanced sentiment analysis.
