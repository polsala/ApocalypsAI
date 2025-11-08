# Emoji Calendar Utility

`emoji-calendar` prints a month calendar where:

* Saturdays are marked with **🛸**
* Sundays are marked with **☀️**
* Pre‑defined holidays get a special emoji (e.g., New Year's Day 🎉, Christmas 🎄)

## Installation

The utility is self‑contained – just copy the `src/` folder into your project or run it directly from the repository.

```bash
python -m utils.emoji-calendar.src.emoji_calendar <year> <month>
```

## Example

```bash
$ python -m utils.emoji-calendar.src.emoji_calendar 2025 1
      1🎉  2  3🛸  4☀️
 5  6  7  8  9 10🛸 11☀️
12 13 14 15 16 17🛸 18☀️
19 20 21 22 23 24🛸 25☀️
26 27 28 29 30 31🛸   
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/emoji-calendar/tests
```
