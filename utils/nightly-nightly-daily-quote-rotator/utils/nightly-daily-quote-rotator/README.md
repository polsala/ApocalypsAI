# Nightly Daily Quote Rotator

**What it does**

- Stores a curated list of whimsical quotes.
- Returns a *deterministic* quote for the current day (or any supplied date).
- No external network access – everything lives locally.

**Why it’s useful**

- Add a daily dose of inspiration to CI pipelines, terminal prompts, or Slack bots.
- Completely offline, making it safe for restricted environments.
- Simple CLI that can be invoked from any script.

**Installation**

```bash
# Clone the repository (or copy the folder) and add it to your PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$(pwd)/utils/nightly-daily-quote-rotator/src"
```

**Usage**

```bash
# Print today’s quote
python -m quote_rotator

# Print a quote for a specific date (YYYY-MM-DD)
python -m quote_rotator --date 2023-01-01
```

**Running the tests**

```bash
cd utils/nightly-daily-quote-rotator
pytest -q
```
