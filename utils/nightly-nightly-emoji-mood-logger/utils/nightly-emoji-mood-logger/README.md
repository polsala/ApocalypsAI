# nightly‑emoji‑mood‑logger

## Overview

`nightly-emoji-mood-logger` is a tiny, self‑contained Python utility that converts a given piece of text into an emoji‑enhanced version. It uses a static, curated mapping of common words and phrases to emojis, making it **offline**, **deterministic**, and **instant**.

## Features

- **Zero external dependencies** – only the Python standard library.
- **Deterministic output** – the same input always yields the same emoji‑rich string.
- **CLI & library usage** – import the `translate` function or run the script directly.
- **Comprehensive tests** – offline unit tests with no network calls.

## Installation

Copy the `utils/nightly-emoji-mood-logger` folder into your project and run:

```bash
python -m utils.nightly-emoji-mood-logger.src.emoji_mood "I love coding"
```

## Usage

### As a library

```python
from utils.nightly-emoji-mood-logger.src.emoji_mood import translate

print(translate("I love coding"))
# Output: "I ❤️ 💻"
```

### As a CLI

```bash
python -m utils.nightly-emoji-mood-logger.src.emoji_mood "Feeling happy and excited"
# Output: "Feeling 😊 and 🤩"
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-mood-logger/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
