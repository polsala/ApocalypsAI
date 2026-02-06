# nightly-ssh-key-expiry-checker

Checks SSH authorized_keys for keys with expiry dates and warns about expired ones.

## Usage

```bash
./src/main.sh [path_to_authorized_keys]
```

If no path is provided, defaults to `~/.ssh/authorized_keys`.

The script looks for comments containing `expires=YYYY-MM-DD`. If the date is in the past relative to the current date (or `CURRENT_DATE` env var), it prints a warning and exits with status 1.

## Example

```bash
$ ./src/main.sh
Expired key: user@example.com (expires=2022-12-31)
```

## Testing

Run `bash tests/test_main.sh`.
