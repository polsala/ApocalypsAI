# nightly-commit-emoji-annotator

A whimsical Bash utility that reads git commit messages (from stdin or `git log`) and prefixes each line with an emoji representing the type of change.

## Usage

```sh
git log --pretty=%s | ./src/commit-emoji.sh
```

Or pipe any list of commit messages:

```sh
cat commits.txt | ./src/commit-emoji.sh
```

## How it works

The script looks for common conventional commit prefixes and maps them to emojis:

- `feat:` → ✨
- `fix:` → 🐛
- `docs:` → 📚
- `chore:` → 🧹
- `refactor:` → ♻️
- otherwise → 🤔

## Testing

Run the provided test script:

```sh
bash tests/test_commit_emoji.sh
```

It will verify that sample inputs produce the expected emoji‑annotated output.

## License

MIT
