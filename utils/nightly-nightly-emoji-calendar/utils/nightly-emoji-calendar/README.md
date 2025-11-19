# Nightly Emoji Calendar

A tiny, self‑contained Python utility that prints a month calendar where every day is suffixed with an emoji that reflects the day of the week.

## Emojis used
| Weekday | Emoji |
|---------|-------|
| Monday  | 🌞 |
| Tuesday | 🌜 |
| Wednesday | 🌟 |
| Thursday | 🌈 |
| Friday  | 🍀 |
| Saturday| 🎉 |
| Sunday  | 🌙 |

## Usage
```bash
python -m utils.nightly-emoji-calendar.src.calendar <year> <month>
```
Example (February 2023):
```text
   1🌈 2🍀 3🎉 4🌙
5🌞 6🌜 7🌟 8🌈 9🍀 10🎉 11🌙
12🌞 13🌜 14🌟 15🌈 16🍀 17🎉 18🌙
19🌞 20🌜 21🌟 22🌈 23🍀 24🎉 25🌙
26🌞 27🌜 28🌟
```

## Running the tests
```bash
python -m unittest discover -s utils/nightly-emoji-calendar/tests
```

## License
MIT – see the root `LICENSE` file.
