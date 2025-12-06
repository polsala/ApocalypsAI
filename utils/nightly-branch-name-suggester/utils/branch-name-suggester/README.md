# Branch Name Suggester

Utility to generate clean kebab‑case git branch names from a short description or issue title.

## Usage

```bash
python -m src.main "Add user authentication" [--issue 42]
```

- Without `--issue` the output will be:
  ```
  add-user-authentication
  ```
- With `--issue 42` the output will be:
  ```
  42-add-user-authentication
  ```

## How it works

1. Lower‑cases the input string.
2. Replaces any sequence of non‑alphanumeric characters with a single hyphen.
3. Strips leading/trailing hyphens.
4. Optionally prefixes the result with the supplied issue number followed by a hyphen.

The implementation lives in `src/main.py` and can also be imported as a module.

## Tests

Run the test suite with:

```bash
pytest -q
```

All tests are deterministic and run offline.
