# Nightly Emoji Calendar

A tiny utility that prints a month calendar where each day is replaced by a whimsical emoji representing its weekday.

## Emojis

- Monday: 🌞
- Tuesday: 🚀
- Wednesday: 📚
- Thursday: 🍕
- Friday: 🎉
- Saturday: 🛌
- Sunday: ☕️

## Usage

```sh
python -m src.emoji_calendar <year> <month>
```

Example:

```sh
python -m src.emoji_calendar 2023 2
```

Outputs a grid of emojis.

## Testing

Run the bundled tests with:

```sh
python -m unittest discover -s tests
```

All tests are deterministic and offline.
