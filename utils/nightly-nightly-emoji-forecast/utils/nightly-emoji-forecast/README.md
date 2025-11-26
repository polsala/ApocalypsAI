# nightly-emoji-forecast

A whimsical CLI that returns an emoji‑based weather forecast for any date. The forecast is deterministic: the same date always yields the same emoji, making it perfect for jokes, commit messages, or daily stand‑ups.

## Usage

```sh
python -m utils.nightly-emoji-forecast.src.forecast [YYYY-MM-DD]
```

If no date is supplied, today’s date is used.

## Example

```sh
$ python -m utils.nightly-emoji-forecast.src.forecast 2023-01-01
🌧️ Rainy
```

## How it works

The utility maps the ordinal value of the date to a small list of emoji forecasts using a simple modulo operation. No external APIs or data files are required.

## Testing

Run the tests with:

```sh
pytest utils/nightly-emoji-forecast/tests
```
