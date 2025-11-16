# Nightly Quote of the Day

A whimsical utility that returns an uplifting quote for the given date. No external network calls; uses a static list of quotes and deterministic selection based on the day of the year. Ideal for adding a daily morale boost to CI logs, Slack bots, or terminal prompts.

## Usage

```bash
python -m utils.nightly-quote-of-the-day.src.quote [YYYY-MM-DD]
```

If no date is supplied, today’s date is used.

## API

- `get_quote(date: datetime.date | None = None) -> str`

## Testing

Run `pytest` in the utility folder.
