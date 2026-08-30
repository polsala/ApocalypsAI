# nightly-env-var-sanitizer

Utility that scans the current environment variables and redacts values of variables that look like secrets (e.g., containing KEY, TOKEN, PASS, SECRET, PWD, CRED). It prints a sanitized list to **stdout** or writes it to a file.

## Usage

```sh
# Print sanitized environment to stdout
./src/sanitize_env.sh

# Write sanitized environment to a file
./src/sanitize_env.sh -o sanitized.env
```

### Options

- `-o <file>` or `--output <file>` – write the sanitized output to the specified file instead of stdout.

### How it works

The script looks at each environment variable name and checks if it contains any of the following case‑insensitive substrings:

- `KEY`
- `TOKEN`
- `PASS`
- `SECRET`
- `PWD`
- `CRED`

If a match is found, the value is replaced with `[REDACTED]`. All other variables are printed unchanged.

## Example

```sh
export API_TOKEN="supersecret"
export DB_PASSWORD="hunter2"
export USERNAME="alice"

./src/sanitize_env.sh
```

Output:

```
API_TOKEN=[REDACTED]
DB_PASSWORD=[REDACTED]
USERNAME=alice
... (other vars)
```

## Testing

Run the test suite with:

```sh
bash tests/test_sanitize_env.sh
```

The tests set up mock environment variables, invoke the script, and verify that secret variables are redacted while normal variables remain intact.
