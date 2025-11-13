# Moon Phase Notifier

`moon-phase-notifier` is a tiny, dependency‑free Python utility that tells you the lunar phase for any date. It’s handy for photographers, gardeners, tide‑watchers, or anyone who likes to plan around the moon.

## Features

- **Deterministic**: Uses a pure‑Python algorithm (Conway’s) – no external APIs.
- **CLI**: `python -m moon_phase [YYYY-MM-DD]` (defaults to today).
- **Library**: Import `moon_phase` function in your own scripts.
- **Zero dependencies** – only the Python standard library.

## Usage

```bash
$ python -m moon_phase 2023-10-28
Moon phase on 2023-10-28: Full Moon
```

If no date is supplied, the current local date is used.

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/moon-phase-notifier/tests
```

## License

MIT
