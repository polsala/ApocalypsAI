# Daily Quote Rotator

**What it does**

- Stores a list of inspirational quotes in a plain‑text file.
- Keeps track of the last date a quote was shown and the current index in a tiny JSON state file.
- When run, it prints *today's* quote, advancing to the next one only once per calendar day.

**Why it’s useful**

- Gives community members a fresh burst of motivation each day without any network calls.
- Fully offline, deterministic, and requires only the Python standard library.
- Easy to embed in a daily‑morning script, a terminal prompt, or a GitHub Action.

**Usage**

```bash
# From the repository root
python -m utils/daily-quote-rotator/src/quote_rotator
```

The command prints the quote for the current day and updates the internal state.

**Structure**

- `quotes.txt` – one quote per line.
- `state.json` – automatically created/updated; you can delete it to reset the rotation.
- `src/quote_rotator.py` – the implementation.
- `tests/` – deterministic unit tests that mock the current date.
