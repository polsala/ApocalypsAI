# Nightly Zen Quote of the Day

Utility that returns a deterministic "Zen" quote based on the current date. No network calls; uses a built‑in list of quotes and a simple hash of the ISO date to pick one. Handy for adding a daily inspirational line to scripts, CI logs, or terminal prompts.

## Usage

```bash
python -m src.zen_quote
# → "The obstacle is the path."
```

Or import `get_quote` in Python:

```python
from src.zen_quote import get_quote
print(get_quote())
```
