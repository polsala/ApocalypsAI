# Deterministic Passphrase Generator

Utility that deterministically generates a password from a master phrase using SHA‑256. Useful for creating reproducible passwords without storing them.

## Usage

```bash
python -m utils.deterministic-passphrase-generator.src.generator "my secret phrase" --length 16
```

Outputs a 16‑character password.

## How it works

- Takes the master phrase, encodes UTF‑8.
- Computes SHA‑256 hash.
- Base64‑url‑encodes the hash.
- Truncates to the requested length.

## Tests

Run with `pytest`:

```bash
pytest utils/deterministic-passphrase-generator/tests
```
