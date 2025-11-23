# Nightly Emoji Mood Logger

## Overview

`nightly-emoji-mood-logger` provides a single function `get_mood_emoji(text: str) -> str` that returns an emoji representing the perceived mood of the supplied text.

* **Happy** – `😊` – triggered by words like *happy, joy, love, great, awesome*.
* **Sad** – `😢` – triggered by words like *sad, bad, terrible, hate, upset*.
* **Neutral** – `😐` – default when no clear sentiment is detected.

The implementation is deliberately lightweight and deterministic – no external APIs, no randomness – making it perfect for offline scripts, CI pipelines, or as a playful addition to commit‑message hooks.

## Installation

The utility is pure Python and has **no third‑party dependencies**. Simply copy the `src/` directory into your project or import it directly from the repository.

```bash
# Example: add to PYTHONPATH or install as a package
cp -r utils/nightly-emoji-mood-logger/src /your/project/
```

## Usage

```python
from logger import get_mood_emoji

print(get_mood_emoji("I love the new feature!"))  # 😊
print(get_mood_emoji("The build failed again...")) # 😢
print(get_mood_emoji("Refactored module"))        # 😐
```

## Testing

Run the bundled tests with `pytest`:

```bash
cd utils/nightly-emoji-mood-logger
pytest -q
```

All tests are deterministic and run offline.
