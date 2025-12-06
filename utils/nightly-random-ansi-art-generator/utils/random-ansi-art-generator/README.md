# Random ANSI Art Generator

A whimsical utility that prints a random ANSI‑colored ASCII art piece to the terminal. Great for adding flair to scripts, commit messages, or just brightening your day.

## Features

- Zero external dependencies (uses only the Python standard library).
- 5 built‑in art pieces with vibrant colors.
- Simple CLI: `python -m src.art_generator` (run from the utility folder) or `python src/art_generator.py`.

## Usage

```bash
$ cd utils/random-ansi-art-generator
$ python src/art_generator.py
```

Will output something like:

```
\033[31m  /\_/\  \033[0m
\033[31m ( o.o ) \033[0m
\033[31m  > ^ <  \033[0m
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s tests
```
