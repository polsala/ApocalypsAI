# nightly-env-var-diff

Utility to compare two `.env` files and report added, removed, and changed environment variables.

## Usage

```sh
./diff_env.sh <old.env> <new.env>
```

The script prints three optional sections:

- **Added variables:** keys present only in the new file.
- **Removed variables:** keys present only in the old file.
- **Changed variables:** keys present in both files but with different values, shown as `key: old => new`.

## How it works

1. Strips comments and empty lines.
2. Sorts entries for reliable comparison.
3. Uses `comm` to find added/removed keys.
4. Checks intersecting keys for value changes.

## Testing

Run the test suite with:

```sh
bash tests/test_diff_env.sh
```
