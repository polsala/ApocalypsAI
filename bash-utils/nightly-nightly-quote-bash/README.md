# nightly-quote-bash

A whimsical Bash utility that prints a random inspirational quote from a bundled list or a custom `quotes.txt` file.

## Usage

```bash
./src/quote.sh
```

If a `quotes.txt` file exists in the current directory, the script will pick a random line from it; otherwise it falls back to a default set of quotes.

## Testing

```bash
bash tests/test_quote.sh
```
