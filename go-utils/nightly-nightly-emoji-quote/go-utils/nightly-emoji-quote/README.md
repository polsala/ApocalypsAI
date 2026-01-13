# nightly-emoji-quote

Prints a random uplifting quote with a matching emoji, perfect for brightening your terminal.

## Usage

```bash
go run .
```

or build a binary:

```bash
go build -o emoji-quote
./emoji-quote
```

The program outputs a single line like:

````
ð The best way to predict the future is to create it.
````

You can set the `RANDOM_SEED` environment variable to a fixed integer to get deterministic output for testing or scripting.

## Features

- Randomly selects from a curated list of quotes.
- Each quote is paired with an emoji that reflects its tone.
- Lightweight, no external dependencies.

## License

MIT
