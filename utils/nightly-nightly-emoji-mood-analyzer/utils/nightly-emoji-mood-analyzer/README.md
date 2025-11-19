# Nightly Emoji Mood Analyzer

## Overview

`emoji-mood-analyzer` is a lightweight, self‑contained Python utility that:

1. **Translates** common ASCII emoticons (e.g., `:)`, `:(`, `:D`) into their Unicode emoji equivalents.
2. **Counts** how many happy, sad, and surprised moods appear in a given text.
3. **Prints** a concise, human‑readable report.

The tool is deliberately whimsical yet useful for developers who want to quickly gauge the emotional tone of logs, commit messages, or chat archives.

## Installation & Usage

```bash
# From the repository root
python -m utils.nightly-emoji-mood-analyzer.src.analyzer <path-to-text-file>
```

The script prints the transformed text followed by a mood summary, e.g.:

```
Transformed Text:
I love this! 😄
But sometimes it fails... 😞

Mood Summary:
  Happy: 1
  Sad:   1
  Surprised: 0
```

## Design

* **Pure Python 3.11** – no external dependencies.
* **Deterministic tests** – all I/O is mocked, ensuring offline execution.
* **Self‑contained** – everything lives under `utils/nightly-emoji-mood-analyzer/`.

## License

MIT – see the top‑level LICENSE file.
