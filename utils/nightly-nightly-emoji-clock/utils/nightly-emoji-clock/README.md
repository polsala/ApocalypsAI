# Nightly Emoji Clock

A tiny utility that turns a time into a sequence of clock‑face emojis.

## How it works

- Hours are represented by the standard clock emojis 🕛 (12 am) through 🕚 (11 pm).
- Minutes are rounded down to the nearest 5‑minute block and shown with the same set of emojis.
- If no time is supplied, the current local time is used.

## Usage

```sh
python -m utils.nightly-emoji-clock.src.emoji_clock          # uses current time
python -m utils.nightly-emoji-clock.src.emoji_clock --time 14:23
```

## Example

```
$ python -m utils.nightly-emoji-clock.src.emoji_clock --time 09:17
🕘🕐
```

The first emoji is the hour (09 am → 🕘), the second is the minute rounded down to the nearest 5 minutes (15 min → 🕐).

## License

MIT
