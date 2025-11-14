# Nightly Emoji Mood Analyzer

A tiny, self‑contained Python utility that scans a piece of text for emojis and determines an overall mood:

- **happy** – more positive emojis than negative ones
- **sad** – more negative emojis than positive ones
- **neutral** – equal counts or no emojis at all

## Features

- Zero external dependencies – pure standard library.
- Simple CLI (`python -m src.emoji_mood "Your text"`).
- Programmatic API via `analyze_mood(text: str) -> str`.
- Fully tested with deterministic offline unit tests.

## Installation & Usage

```bash
# Clone the repository (or just copy the utils folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-emoji-mood-analyzer

# Run the CLI
python -m src.emoji_mood "I love this! 😄👍"
# → happy
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s tests
```

---

*Created by the ApocalypsAI Nightly Integrator agent.*
