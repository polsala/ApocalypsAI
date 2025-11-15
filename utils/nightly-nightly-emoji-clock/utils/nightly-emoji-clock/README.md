# Nightly Emoji Clock

`nightly-emoji-clock` is a tiny utility that turns the current time into a string of emojis. It can be used in logs, chat bots, or anywhere a playful timestamp is welcome.

## Features

- No external dependencies.
- Deterministic output for a given `datetime`.
- Simple CLI: `python -m utils.nightly-emoji-clock.src.emoji_clock`.

## Usage

```bash
python -m utils.nightly-emoji-clock.src.emoji_clock
```

Will print something like:

```
1️⃣3️⃣⏰4️⃣5️⃣
```

(Actual output depends on the current time.)

## Implementation

The core function `get_emoji_time(dt)` maps each digit of the hour and minute to its corresponding emoji digit (0️⃣‑9️⃣) and keeps the colon separator.

## Testing

Run the tests with:

```bash
python -m unittest discover utils/nightly-emoji-clock/tests
```
