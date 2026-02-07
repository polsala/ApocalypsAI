# nightly-commit-emoji-annotator

Adds emojis to git commit messages based on conventional commit types.

## Usage

```sh
git log --pretty=format:"%s" | ./src/annotate.sh
```

The script reads commit titles from **stdin** and prints each line prefixed with an appropriate emoji.

## Mapping

- `feat`: ✨
- `fix`: 🛠️
- `docs`: 📚
- `test`: ✅
- `chore`: 🧹
- `refactor`: ♻️
- `perf`: 🚀
- `style`: 🎨
- `build`: 🏗️
- `ci`: 🤖
- `revert`: ⏪
- *any other*: 🔹

## License

MIT
