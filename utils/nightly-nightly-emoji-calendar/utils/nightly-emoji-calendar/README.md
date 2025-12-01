# nightly‑emoji‑calendar

**What it does**

`nightly-emoji-calendar` prints a simple month calendar where every day is replaced by an emoji that corresponds to the weekday:

| Weekday | Emoji |
|---------|-------|
| Monday    | 🌞 |
| Tuesday   | 🌜 |
| Wednesday | 🌟 |
| Thursday  | 🌈 |
| Friday    | 🎉 |
| Saturday  | 🛌 |
| Sunday    | 🍳 |

The utility is completely self‑contained, requires only the Python standard library, and can be invoked from the command line:

```bash
python -m utils.nightly-emoji-calendar.src.emoji_calendar [--year YYYY] [--month MM]
```

If `--year` and `--month` are omitted, the current month (according to the system clock) is used.

**Why it’s useful**

- Gives a quick visual cue of the upcoming week’s vibe.
- Fun for terminal lovers, bots, or any script that wants a lightweight “emoji forecast”.
- No external network calls – perfect for offline CI runs.

**Testing**

The package ships with deterministic unit tests that mock the current date, ensuring the output is reproducible.
