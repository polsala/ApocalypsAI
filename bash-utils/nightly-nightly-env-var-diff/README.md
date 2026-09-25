# nightly-env-var-diff

Utility to compare two `.env` files and list added, removed, and modified environment variables.

## Usage

```sh
./src/env_diff.sh path/to/old.env path/to/new.env
```

The script prints three optional sections:

* **Added** – variables present only in the second file.
* **Removed** – variables present only in the first file.
* **Modified** – variables present in both files but with different values.

## Example

```sh
cat > old.env <<EOF
VAR1=foo
VAR2=bar
VAR3=baz
# comment line
EOF

cat > new.env <<EOF
VAR1=foo
VAR2=qux
VAR4=quux
EOF

./src/env_diff.sh old.env new.env
```

Output:

```
Added:
VAR4=quux

Removed:
VAR3=baz

Modified:
VAR2: bar -> qux
```

The utility is written in pure Bash and requires Bash 4+ for associative arrays.
