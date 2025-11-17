# Quote of the Day

A tiny offline utility that returns a deterministic **Quote of the Day** based on the current date. Optionally filter by tag (e.g., `inspiration`, `humor`). No network calls; all quotes are baked in.

## Installation

```bash
pip install .
```

*(Or copy the `src/quote_of_the_day.py` into your project.)*

## Usage

```bash
python -m quote_of_the_day          # prints today's quote
python -m quote_of_the_day --tag humor   # prints a humorous quote for today
```

## API

```python
from quote_of_the_day import get_quote

quote = get_quote()          # -> str
quote = get_quote(tag="inspiration")
```

## Testing

```bash
pytest -q utils/nightly-quote-of-the-day/tests
```
