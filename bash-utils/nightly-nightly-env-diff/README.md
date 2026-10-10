# Nightly Env Diff

**Utility:** Compare two `.env` files and get a clear report of what variables were added, removed, changed, or stayed the same.

## Usage
```bash
./src/env_diff.sh <old.env> <new.env>
```

- `<old.env>` – the original environment file.
- `<new.env>` – the updated environment file.

The script prints four optional sections (only shown if there is at least one entry):

- **Added** – variables present only in the new file.
- **Removed** – variables present only in the old file.
- **Changed** – variables present in both files but with different values.
- **Unchanged** – variables present in both files with identical values.

## Example
```bash
cat old.env
FOO=1
BAR=2
BAZ=old

cat new.env
FOO=1
BAR=3
NEWVAR=hello
BAZ=old

./src/env_diff.sh old.env new.env
```
Output:
```
Added:
  NEWVAR

Changed:
  BAR

Unchanged:
  FOO
  BAZ
```

## Requirements
- Bash 4+ (associative arrays are used).
- No external dependencies.

## Testing
Run the provided test script:
```bash
cd tests && ./test_env_diff.sh
```
It creates temporary `.env` files, runs the diff, and verifies the output.
