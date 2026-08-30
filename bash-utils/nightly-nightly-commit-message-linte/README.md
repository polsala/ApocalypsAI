# nightly-commit-message-linter

Utility to lint Git commit messages according to a simple style guide.

## Usage

```sh
cat commit.txt | ./src/main.sh
# or
./src/main.sh commit.txt
```

The script exits with status **0** if the message passes all checks, otherwise non‑zero and prints the reasons.

## Checks performed

- Subject line ≤ 50 characters.
- Subject line starts with a capital letter and does not end with a period.
- Body lines ≤ 72 characters.
- At least one line contains an issue reference like `#123`.
