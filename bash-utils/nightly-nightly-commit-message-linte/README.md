# nightly-commit-message-linter

Utility to lint Git commit messages according to conventional rules.

## Usage

```sh
cat COMMIT_MSG | ./src/lint_commit.sh
# or
./src/lint_commit.sh path/to/COMMIT_MSG
```

The script checks:

- Subject line ≤ 50 characters
- Subject starts with a capital letter
- Subject does not end with a period
- Body lines ≤ 72 characters
- No trailing whitespace in any line

It exits with code **0** if the message passes, otherwise **1** and prints errors to stderr.
