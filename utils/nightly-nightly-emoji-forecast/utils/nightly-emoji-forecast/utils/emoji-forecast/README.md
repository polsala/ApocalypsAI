# Emoji Forecast

**What it does**

`emoji-forecast` generates a single line of emoji “weather” based on the current date. The algorithm is deterministic – the same date always yields the same forecast – making it safe for tests and reproducible builds.

**Why it’s useful**

- Adds a light‑hearted visual cue to daily logs or CI output.
- No network calls, no external data – completely offline.
- Zero dependencies, pure Python 3.11.

**Installation**

```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-emoji-forecast
```

**Usage**

```bash
python -m utils.emoji-forecast.src.forecast
# Example output: 🌤️ 🌈 ☔️
```

**Running the tests**

```bash
pytest utils/nightly-emoji-forecast/utils/emoji-forecast/tests
```
