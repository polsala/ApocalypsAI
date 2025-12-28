# nightly-commit-emoji-adder

Adds a relevant emoji to a Git commit message based on its content.

## Usage

```bash
# Read from a commit message file and output modified message
./src/commit-emoji.sh path/to/COMMIT_MSG

# Or pipe a commit message
cat COMMIT_MSG | ./src/commit-emoji.sh

# Write back to the file
./src/commit-emoji.sh -w path/to/COMMIT_MSG
```

## Supported Keywords

- `feat` → 🎉
- `fix` → 🐛
- `docs` → 📚
- `style` → ✨
- `refactor` → 🔧
- `test` → ✅
- `chore` → 🔄

If no keyword is found, the message is left unchanged.

## License

MIT
