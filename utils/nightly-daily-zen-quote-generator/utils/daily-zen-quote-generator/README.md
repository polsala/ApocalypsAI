# Daily Zen Quote Generator

A tiny, self‑contained utility that prints a deterministic *quote of the day*.

## What it does
- Stores a short list of inspirational quotes.
- Chooses a quote based on the current date (using the date’s ordinal modulo the number of quotes).
- Guarantees the same quote for the same calendar day, without any network calls.

## Why it’s useful
- Add a pleasant line to your terminal start‑up (`~/.bashrc`, `~/.zshrc`).
- Feed a Slack/Discord bot with a daily message.
- Use in CI pipelines to embed a friendly reminder.

## Usage
```bash
python -m src.main   # prints today’s quote
```
Or import the function in your own code:
```python
from src.main import get_quote
print(get_quote())
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
The tests mock the system date to stay deterministic and offline.
