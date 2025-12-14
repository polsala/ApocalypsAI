# nightly-emoji-commit-visualizer

Displays git commit messages with expressive emojis based on keywords.

## Usage

```sh
./src/emoji_commit_visualizer.sh [git-range]
```

If no range is provided, the script defaults to `HEAD`.

The script reads commit messages via `git log --pretty=%s` and prefixes each line with an emoji:

- `fix` → 🛠️
- `add` → ✨
- `remove` → ❌
- `refactor` → ♻️
- `docs` → 📚
- `test` → ✅
- otherwise → 🔎

## Example

```sh
$ ./src/emoji_commit_visualizer.sh
🛠️ Fix typo in README
✨ Add new feature X
❌ Remove deprecated API
♻️ Refactor module Y
📚 Update docs for Z
✅ Write tests for A
🔎 Miscellaneous cleanup
```

## Testing

Run the test suite:

```sh
bash tests/test_emoji_commit_visualizer.sh
```
