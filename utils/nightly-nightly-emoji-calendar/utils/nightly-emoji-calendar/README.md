# Nightly Emoji Calendar

A whimsical utility that generates a markdown calendar for any month, decorating each day with an emoji that represents its weekday.

## Features

- Deterministic, offline generation.
- Emoji legend:
  - Monday: 🌞
  - Tuesday: 🚀
  - Wednesday: 🌱
  - Thursday: 🔥
  - Friday: 🎉
  - Saturday: 🛌
  - Sunday: ☕
- Can be used in scripts, documentation, or just for fun.

## Usage

```sh
python -m nightly_emoji_calendar src/calendar.py [--year YEAR] [--month MONTH]
```

If `--year` or `--month` are omitted, the current year/month are used.

## Example

Running for March 2023 produces:

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|  |  | 🌱 1 | 🔥 2 | 🎉 3 | 🛌 4 | ☕ 5 |
| 🌞 6 | 🚀 7 | 🌱 8 | 🔥 9 | 🎉 10 | 🛌 11 | ☕ 12 |
| 🌞 13 | 🚀 14 | 🌱 15 | 🔥 16 | 🎉 17 | 🛌 18 | ☕ 19 |
| 🌞 20 | 🚀 21 | 🌱 22 | 🔥 23 | 🎉 24 | 🛌 25 | ☕ 26 |
| 🌞 27 | 🚀 28 | 🌱 29 | 🔥 30 | 🎉 31 |  |  |

## License

MIT
