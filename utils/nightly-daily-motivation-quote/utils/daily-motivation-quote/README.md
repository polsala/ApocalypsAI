# Daily Motivation Quote

A whimsical utility that prints a random motivational quote from a built‑in collection. No external dependencies, works offline.

## Features

- Random quote selection
- Optional category filter (`inspiration`, `humor`, `wisdom`)
- Simple CLI: `python -m daily_motivation_quote` (or `python src/quote.py`)

## Installation

Just copy the folder into your repository and run with Python 3.11.

## Usage

```sh
$ python -m daily_motivation_quote
💡 "The only limit to our realization of tomorrow is our doubts of today." – Franklin D. Roosevelt
```

Filter by category:

```sh
$ python -m daily_motivation_quote --category humor
😂 "I am not lazy, I am on energy‑saving mode." – Anonymous
```

## Testing

```sh
$ python -m unittest discover -s utils/daily-motivation-quote/tests
```
