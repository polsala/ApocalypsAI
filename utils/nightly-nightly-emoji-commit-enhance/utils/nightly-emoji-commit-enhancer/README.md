# Nightly Emoji Commit Enhancer

## Overview

`emoji-commit-enhancer` scans a Git commit message for common keywords (e.g., *fix*, *feat*, *docs*, *test*, *refactor*) and prepends an appropriate emoji. The tool is completely offline, has zero external dependencies, and can be invoked as a CLI or imported as a library.

## Installation

```bash
# Clone the repository (or copy the folder) and install the package locally
pip install -e utils/nightly-emoji-commit-enhancer
```

## Usage

### As a library

```python
from emoji_committer import enhance_message

original = "fix typo in README"
print(enhance_message(original))  # ➜ "🐛 fix typo in README"
```

### As a CLI

```bash
python -m emoji_committer "Add new feature for user login"
# Output: ✨ Add new feature for user login
```

## How it works

The utility maintains a small mapping of keywords to emojis. It performs a case‑insensitive search for any keyword; the first match wins. If no keyword is found, the original message is returned unchanged.

## Testing

Run the test suite with:

```bash
pytest utils/nightly-emoji-commit-enhancer/tests
```

All tests are deterministic and use no network calls.
