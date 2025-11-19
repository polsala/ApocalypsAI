# Nightly Emoji Forecast

`nightly-emoji-forecast` is a tiny, self‑contained Python utility that turns any date (ISO‑format `YYYY‑MM‑DD`) into a deterministic emoji "forecast".  The mapping is purely based on a hash of the date, so it works offline and always returns the same emoji for the same date.

## Features

- **Zero external dependencies** – only the Python standard library.
- **Deterministic** – the same input date always yields the same emoji.
- **CLI** – `python -m nightly_emoji_forecast <date>` prints the emoji.
- **Library** – import `get_emoji_for_date` in your own scripts.
- **Tests** – fully covered with offline deterministic tests.

## Usage

```bash
# As a CLI
python -m nightly_emoji_forecast 2025-12-25
# => 🎄

# As a library
from nightly_emoji_forecast import get_emoji_for_date
print(get_emoji_for_date('2025-12-25'))  # 🎄
```

## Implementation Details

The utility hashes the input string with SHA‑256, converts the hex digest to an integer, and selects an emoji from a curated list using modulo arithmetic.  This approach guarantees a uniform distribution without any network calls.

## License

MIT – see the repository LICENSE file.
