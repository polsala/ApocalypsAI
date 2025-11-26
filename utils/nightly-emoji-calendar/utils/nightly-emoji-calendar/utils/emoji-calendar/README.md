# Emoji Calendar

Utility that prints a month calendar where each day of the week is represented by a whimsical emoji.

## Usage

```bash
python -m emoji_calendar 2025 12
```

The command prints a calendar for the given year and month, e.g.:

```
    December 2025    
🌞 🚀 🌱 📚 🎉 🛌 ☕
 1  2  3  4  5  6  7
 8  9 10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31          
```

## Emoji mapping

| Weekday | Emoji |
|---------|-------|
| Monday    | 🌞 |
| Tuesday   | 🚀 |
| Wednesday | 🌱 |
| Thursday  | 📚 |
| Friday    | 🎉 |
| Saturday  | 🛌 |
| Sunday    | ☕ |

The utility is self‑contained, requires only the Python standard library, and includes deterministic offline tests.
