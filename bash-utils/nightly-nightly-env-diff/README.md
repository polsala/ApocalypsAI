# nightly-env-diff

**Utility:** Compare two `.env` files and report which environment variables were added, removed, or changed.

## Usage

```bash
./env_diff.sh <old.env> <new.env>
```

- `<old.env>` – The original environment file.
- `<new.env>` – The updated environment file.

The script prints three optional sections (only if applicable):

- `Added: VAR1 VAR2 ...`
- `Removed: VAR3 VAR4 ...`
- `Changed: VAR5 (old->new) VAR6 (old->new) ...`

## Example

```bash
cat > old.env <<EOF
DB_HOST=localhost
DB_PORT=5432
DEBUG=true
API_KEY=oldkey
EOF

cat > new.env <<EOF
DB_HOST=localhost
DB_PORT=5433
DEBUG=false
NEW_VAR=hello
API_KEY=oldkey
EOF

./env_diff.sh old.env new.env
```

Output:
```
Added: NEW_VAR
Changed: DB_PORT (5432->5433) DEBUG (true->false)
```

## Notes

- Lines starting with `#` are ignored as comments.
- Blank lines are ignored.
- Variable names are case‑sensitive.
- The script exits with status `1` if the number of arguments is not exactly two.
