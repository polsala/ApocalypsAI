# nightly-env-var-diff

Utility to compare two `.env` files and report added, removed, and modified environment variables.

## Usage

```sh
./src/diff_env.sh <old.env> <new.env>
```

- `<old.env>` – the original environment file.
- `<new.env>` – the updated environment file.

The script prints three optional sections:

- **Added:** variables present only in the new file.
- **Removed:** variables present only in the old file.
- **Modified:** variables present in both files but with different values.

If a section has no entries it is omitted from the output.

## Example

```sh
cat > old.env <<'EOF'
DB_HOST=localhost
DB_PORT=5432
API_KEY=oldkey
EOF

cat > new.env <<'EOF'
DB_HOST=localhost
DB_PORT=5433
API_KEY=newkey
NEW_VAR=hello
EOF

./src/diff_env.sh old.env new.env
```

Output:

```
Added:
NEW_VAR=hello

Modified:
DB_PORT: 5432 -> 5433
API_KEY: oldkey -> newkey
```

## Testing

Run the test suite with:

```sh
bash tests/test_diff_env.sh
```

The tests are deterministic and do not require any external resources.
