# Nightly Emoji Mood Logger

## Overview

`emoji-mood-logger` is a lightweight command‑line tool that translates a brief textual mood description into a single Unicode emoji. It can be used to add a quick emotional tag to logs, commit messages, or any plain‑text communication.

## Installation

```bash
# From the repository root
cd utils/nightly-emoji-mood-logger
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (none required beyond the standard library)
```

## Usage

```bash
python -m src.logger "feeling great after the build"
# Output: 😄
```

## How it works

The script performs a simple keyword lookup against a predefined dictionary of mood words. The first matching keyword determines the emoji. If no keywords match, a neutral face is returned.

## Testing

Run the test suite with:

```bash
pytest -q
```

---

*Created by the ApocalypsAI Nightly Integrator.*
