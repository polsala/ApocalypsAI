# Nightly Fortune Cookie

A tiny utility that prints a random fortune cookie message. Great for adding a splash of inspiration to CI runs, daily scripts, or just for fun.

## Usage

```bash
python -m utils.nightly_fortune_cookie.src.fortune
# or
python utils/nightly-fortune-cookie/src/fortune.py
```

## API

- `get_fortune() -> str`: Returns a random fortune.
- `main()`: Prints a fortune to stdout.

## Testing

Run the tests with `pytest` from the repository root:

```bash
pytest utils/nightly-fortune-cookie/tests
```
