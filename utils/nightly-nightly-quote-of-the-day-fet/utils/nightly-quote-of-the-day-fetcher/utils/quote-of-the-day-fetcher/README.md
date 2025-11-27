# Quote of the Day Fetcher

Utility that prints a random quote from a curated list. It can optionally filter quotes by a tag.

## Installation

The utility is pure Python 3.11 and has no external dependencies. Simply copy the folder into your project or run it directly:

```bash
python -m quote_of_the_day_fetcher.src.main [--tag <tag>]
```

## Usage

- **No arguments** – prints a random quote.
- `--tag <tag>` – limits the selection to quotes that contain the given tag (e.g., `inspiration`, `life`, `humor`).

## Example

```bash
$ python -m quote_of_the_day_fetcher.src.main
"The only limit to our realization of tomorrow is our doubts of today." — Franklin D. Roosevelt
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-quote-of-the-day-fetcher/utils/quote-of-the-day-fetcher/tests
```
