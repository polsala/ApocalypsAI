# Nightly Emoji Annotator

**Utility name:** `nightly-emoji-annotator`

## What it does

`emoji‑annotator` scans a given piece of text and appends a relevant emoji after each recognized keyword. It is deliberately lightweight, has **no external network calls**, and can be used in scripts, CI logs, or just for fun.

## Features

- Keyword → emoji mapping (happy, sad, fire, love, warning, success, error, etc.)
- Simple Python 3.11 implementation, no third‑party dependencies.
- Command‑line interface:
  ```bash
  python -m nightly_emoji_annotator "Build succeeded"
  # → "Build succeeded ✅"
  ```
- Library function `annotate(text: str) -> str` for programmatic use.

## Installation

Copy the `utils/nightly-emoji-annotator` folder into your repository and run the tests to verify the environment. No additional packages are required.

## Usage

```bash
# As a module
python -m nightly_emoji_annotator "The server is on fire!"
# Output: The server is on fire! 🔥

# As a library
from nightly_emoji_annotator import annotate
print(annotate("I am very happy"))
# Output: I am very happy 😊
```

## Testing

```bash
cd utils/nightly-emoji-annotator
python -m unittest discover -s tests
```

## Design notes

- The mapping is deliberately small and deterministic.
- The implementation avoids any I/O beyond `argparse` and `print`.
- Tests use only the standard library; no network or file system side‑effects.
