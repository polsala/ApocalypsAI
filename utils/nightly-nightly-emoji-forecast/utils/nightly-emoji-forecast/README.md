# Nightly Emoji Forecast

**What it does**

- Reads a JSON weather payload (or uses a built‑in mock).
- Maps each weather condition to a representative emoji.
- Prints a one‑line emoji forecast, e.g. `🌤️  ☔️  🌙`.

**Why it’s useful**

- Gives teams a quick, light‑hearted weather snapshot without leaving the terminal.
- Can be embedded in CI logs, Slack messages, or commit messages.
- Fully offline – the mock data lives inside the utility.

**Installation**

```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no extra deps needed)
```

**Usage**

```bash
python -m utils.nightly-emoji-forecast.src.main [--data path/to/weather.json]
```

If `--data` is omitted, the utility falls back to an internal mock representing a typical day.

**Testing**

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```
