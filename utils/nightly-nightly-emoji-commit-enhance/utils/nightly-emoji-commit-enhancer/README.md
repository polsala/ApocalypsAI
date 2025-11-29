# Nightly Emoji Commit Enhancer

## Overview

`emoji-commit-enhancer` is a lightweight, zero‑dependency Python utility that prepends an appropriate emoji to a git commit message based on its content.  It helps teams add a splash of personality to their history while staying fully offline.

## Features

- Detects common commit intents (feat, fix, docs, refactor, test, chore, style, perf) and maps them to emojis.
- Falls back to a generic wrench emoji when no intent is detected.
- Provides a simple CLI that can be used in a `prepare‑commit‑msg` hook or manually.

## Installation

```bash
# Clone the repository (or copy the folder) and add it to your PATH
pip install .  # optional, the script is pure Python
```

## Usage

```bash
# From the command line
python -m utils.nightly-emoji-commit-enhancer.src.emoji_committer "Add new authentication flow"
# → ✨ Add new authentication flow
```

You can also pipe a message:

```bash
echo "Fix typo in README" | python -m utils.nightly-emoji-commit-enhancer.src.emoji_committer
# → 🐛 Fix typo in README
```

## Integration with Git Hooks

Add the following to `.git/hooks/prepare-commit-msg` (make it executable):

```bash
#!/usr/bin/env bash
# $1 is the path to the temporary commit message file
msg=$(cat "$1")
new_msg=$(python -m utils.nightly-emoji-commit-enhancer.src.emoji_committer "$msg")
echo "$new_msg" > "$1"
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-commit-enhancer/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
