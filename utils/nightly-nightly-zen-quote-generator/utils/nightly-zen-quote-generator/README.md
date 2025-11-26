# Nightly Zen Quote Generator

A tiny utility that prints a deterministic Zen‑style quote for the current day (or any given date). Perfect for adding a moment of calm to your terminal, CI logs, or daily stand‑ups.

## Features

* **Deterministic** – The same date always yields the same quote, without any network calls.
* **Zero dependencies** – Pure Python 3.11 standard library.
* **CLI friendly** – `python -m src.zen` prints today’s quote; optionally pass `YYYY‑MM‑DD`.
* **Embeddable** – Import `get_zen_quote` in your own scripts.

## Usage

```bash
# Print today’s Zen quote
python -m src.zen

# Print quote for a specific date
python -m src.zen 2023-12-31
```

Or in code:

```python
from src.zen import get_zen_quote
print(get_zen_quote())               # today
print(get_zen_quote(date(2024,1,1))) # specific date
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```

All tests are deterministic and run offline.

## License

MIT © ApocalypsAI
