# Emoji Quote of the Day

A tiny utility that prints a random inspirational quote paired with a random emoji. Perfect for adding a splash of joy to terminal sessions, chat bots, or daily emails.

## Usage

```bash
python -m emoji_quote_of_the_day
```

or

```bash
python utils/emoji-quote-of-the-day/src/main.py
```

## How it works

- A short list of quotes and emojis is bundled with the utility.
- `get_emoji_quote()` picks one of each at random.
- The script prints them in the format: `<emoji> <quote>`.

## Testing

Run the tests with:

```bash
python -m unittest discover utils/emoji-quote-of-the-day/tests
```
