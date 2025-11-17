# Nightly Emoji Clock

Utility that prints the current time as a clock‑face emoji. Useful for adding a whimsical timestamp to logs, commit messages, or chat.

## Usage

```sh
python -m utils.nightly-emoji-clock.src.emoji_clock
# or
python utils/nightly-emoji-clock/src/emoji_clock.py
```

Will output something like `🕒`.

## API

```python
get_emoji_time(dt: datetime | None = None) -> str
```

Returns the clock emoji representing the hour of the given datetime (or now).

## Tests

Run with `pytest`:

```sh
pytest utils/nightly-emoji-clock/tests
```
